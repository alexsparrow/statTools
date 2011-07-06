#!/usr/bin/env python

""" This script steers the systematics calculations and outputs a LaTeX
table. The actual calculations are performed in the C++ files predict.C
"""
import ROOT as r
import math
import config as cfg
import utils
from likelihood import OneLeptonSimple
from multiprocessing import Pool, TimeoutError
import json
import time, os, copy
from limit_utils import toys, capture, quantiles

import pprint

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def setupLimit(actions, maxPoints):
    def plot(data, results):
        c = r.TCanvas("test")
        nbins = len(data["NObserved"])
        obs = r.TH1D("obs", "obs", nbins, 0.5, nbins+0.5)
        pred = r.TH1D("pred", "pred", nbins, 0.5, nbins+0.5)
        for idx, b in enumerate(data["NObserved"]):
            obs.SetBinContent(idx+1, b)
            pred.SetBinContent(idx+1, results[idx].predicted())
            pred.SetBinError(idx+1, math.sqrt(results[idx].predicted()))
        pred.SetLineColor(r.kRed)
        obs.Draw("hist")
        pred.Draw("hist e same")
        c.SaveAs("pred_obs.pdf")

    # Get the background prediction per bin
    data = utils.getZeroData()
    mc = utils.getZeroMC()
    results = utils.makePredictions(data)

    systs = utils.getSystematicsBkg()

    Rshifts = {}
    for name, scaled in systs:
        Rshifts[name] = utils.getSystematicShiftsR(mc, scaled[0], scaled[1])

    print "Extracting signal data..."
    susyEff = utils.getZeroMCSignal()
    effSysts = utils.getSystematicsSignalEff()

    susyPoints = []
    for idx, p in enumerate(susyEff):
        drop = None
        for name, scaled in effSysts:
            shift = utils.getSystematicShiftsEff(p, scaled[0], scaled[1])
            if not shift:
                drop = "Missing syst %s" % name
                break
            else: p["eff%sShift" % name] = shift
        if sum(p["efficiencies"]) < 0.05:
            drop = "Low efficiency sum"
        elif p["m0"] < 500 and p["m1/2"] < 200:
            drop = "Out of range"
        if drop: print "Dropping point: %d, %d. %s" % (p["m0"], p["m1/2"], drop)
        else: susyPoints.append(p)

    if maxPoints: susyPoints = susyPoints[:maxPoints]
    print "Selecting %d points out of %d" % (len(susyPoints), len(susyEff))

    dataInfo = {
        "NObserved": [b.observed() for b in data]
        }
    background = {
        "NControl" : [b.control() for b in data],
        "R": [b.R() for b in data],
        }

    systematics = {
        "signal" : utils.getSignalSystematics(),
        "background" : utils.getBackgroundSystematics()
        }

    for name, shifts in Rshifts.iteritems():
        background["R%sShift" % name] = shifts

    plot(dataInfo, results)
    return {
        "data" : dataInfo,
        "background" : background,
        "systematics" : systematics,
        "signal" : susyPoints,
        "actions" : actions
        }

def workOnPoint(actions, dataInfo, backgroundInfo, systematics, signalPoint, rootfname):
    r.gROOT.SetBatch(True)
    r.RooRandom.randomGenerator().SetSeed(1)
    #r.RooMsgService.instance().addStream(r.RooFit.DEBUG, r.RooFit.Topic(r.RooFit.Tracing), r.RooFit.ClassName("RooGaussian"))
    if cfg.use_nloxs: signalPoint["xs"] = signalPoint["nloxs"]
    else: signalPoint["xs"] = signalPoint["loxs"]

    rfile = r.TFile(rootfname, "recreate")
    (w, modelConfig, dataset) = OneLeptonSimple(cfg.constants, dataInfo,
                                                backgroundInfo, signalPoint,
                                                systematics)
    w.Print()
    #print signalPoint

    for act in actions:
        if act["name"] == "limit":
            signalPoint[act["method"]] = capture(w, modelConfig, dataset, act["cl"], act["method"],
                                                 signalPoint)
        elif act["name"] == "toys":
            signalPoint["toys"] = []
            for expt_w, expt_dset in toys(w, modelConfig, dataset, act["n"], act["cl"]):
                signalPoint["toys"].append(capture(expt_w, modelConfig, expt_dset, act["cl"]))
            limits = [x["limit"][1] for x in signalPoint["toys"]]
            signalPoint["quantiles"] = quantiles(limits, cfg.plusMinus)

        else: raise ValueError("Invalid action: %s" % act["name"])
    rfile.Write()

    return signalPoint

def runLimit(job, fork, timeout, rootfname):
    actions = job["actions"]
    dataInfo = job["data"]
    backgroundInfo = job["background"]
    signalPoints = job["signal"]
    systematics = job["systematics"]
    pointsOut = []
    if fork > 1:
        pool = Pool(processes=fork)
        res = []
        for p in signalPoints:
            args = [actions, dataInfo, backgroundInfo, systematics, p, rootfname]
            res.append(pool.apply_async(workOnPoint, args))
        for result in res:
            try:
                print "Waiting..."
                pointsOut.append(result.get(timeout))
            except TimeoutError:
                continue
    else:
        for p in signalPoints:
            args = [actions, dataInfo, backgroundInfo, systematics, p]
            pointsOut.append(workOnPoint(*args))
    return pointsOut


def options():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option("-s", "--schedule", action = "store_true", default = False)
    parser.add_option("-p", "--points-per-job", action = "store", type="int", default = 20)
    parser.add_option("-r", "--run", action = "store_true", default = False)
    parser.add_option("-f", "--fork", action = "store",  type = "int", default = 8)
    parser.add_option("-b", "--batch-run", action="store", type="string", default = None)
    parser.add_option("-m", "--merge", action="store", type = "string", default = None)
    parser.add_option("-a", "--action", action="store", type = "string", default = "limit")
    parser.add_option("-c", "--confidence-level", action="store", type="float", default = 0.95)
    parser.add_option("-l", "--limit", action="append", dest="limit",
                      choices = ["pl", "clsviatoys"], default=[])
    parser.add_option("-t", "--toys", action="store", type="int", default = None)
    parser.add_option("-T", "--timeout", action = "store", type="int", default=60*60)
    parser.add_option("-o", "--output-file", action = "store", type="string", default = "limit.pkl")
    parser.add_option("-N", "--N-points", action="store", type="int", default=None)
    parser.add_option("-n", "--do-nothing", action="store_true")
    (opts, args) = parser.parse_args()
    if (opts.schedule or opts.run) and not opts.limit and not opts.toys and not opts.do_nothing:
        raise ValueError("Must specify action")
    return (opts, args)

def subJobs(job_dir, njobs, queue = "hepshort.q"):
    import subprocess
    p = subprocess.Popen(["qsub",
                          "-q", queue,
                          "-t", "%d-%d:1" % (1, njobs),
                          "-o", job_dir,
                          "-e", job_dir,
                          "-N", "limits",
                          job_dir+"/run.sh"])
    if p.wait() == 0:
        print "%d jobs submitted successfuly" % njobs

if __name__ == "__main__":
    opts, args = options()
    r.gROOT.LoadMacro("predict.C+")
    actions = []
    for meth in opts.limit:
        actions.append({"name":"limit",
                        "cl":opts.confidence_level,
                        "method": meth})
    if opts.toys:
        actions.append({"name":"toys",
                        "cl":opts.confidence_level,
                        "n" : opts.toys})
    if opts.schedule or opts.run:
        task = setupLimit(actions, opts.N_points)

    if opts.schedule:
        job_dir = "%s/__limits__%s" % (os.getcwd(), time.strftime("%Y%m%d_%H_%M_%S"))
        os.mkdir(job_dir)
        for idx, pts in enumerate(chunks(task["signal"], opts.points_per_job)):
            os.mkdir("%s/%d" % (job_dir, idx+1))
            jobdict = copy.deepcopy(task)
            jobdict["signal"] = pts
            json.dump(jobdict, open("%s/%d/job.json" % (job_dir, idx+1), "w"), indent=0)
            open("%s/run.sh" % job_dir,"w").write("""#!/bin/sh
            source %(cwd)s/envIC2.sh
            cd %(cwd)s
            ./runLimit.py --batch-run %(job_dir)s/${SGE_TASK_ID} --fork %(fork)d --timeout %(timeout)d
            """ % {"cwd": os.getcwd(), "job_dir" : job_dir, "fork" : opts.fork, "timeout" : opts.timeout})
        subJobs(job_dir, idx)
        print "Scheduled %s jobs: %s" % (idx, job_dir)
    elif opts.run or opts.batch_run:
        if opts.batch_run:
            task = json.load(open("%s/job.json" % opts.batch_run))
            print "Starting batch job!"
            ofile = "%s/results.json" % opts.batch_run
            orootfile = "%s/results.root" % opts.batch_run
        else:
            ofile = opts.output_file
            orootfile = opts.output_file.replace(".json", ".root").replace(".pkl", ".root")
        results = runLimit(task, opts.fork, opts.timeout, orootfile)
        json.dump({"results" : results},
                  open(ofile, "w"))
    elif opts.merge:
        if os.path.exists(opts.output_file): raise IOError("Output file exists: %s" % opts.output_file)
        else: print "Dumping to file: %s" % opts.output_file
        files = []
        idx = 1
        while True:
            path = "%s/%d/results.json" % (opts.merge, idx)
            if not os.path.exists(path):
                break
            files += [path]
            idx += 1
        points = []
        for idx, fname in enumerate(files):
            if idx % 10 == 0: print "Scanning file %d/%d" % (idx, len(files))
            pointsToAdd = utils.loadFile(fname)["results"]
            points.extend(pointsToAdd)
            if len(pointsToAdd) == 0:
                print "[WARNING] Empty output file: %d" % idx
        utils.saveFile({"results": points}, opts.output_file)
        print "Dumped %d files with %d points" % (idx -1, len(points))
