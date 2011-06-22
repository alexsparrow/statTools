import ROOT as r
import config as cfg
import os.path

def formatBin(idx):
    if idx < len(cfg.bins) -1:
        return "%d - %d" % (cfg.bins[idx], cfg.bins[idx+1])
    else:
        return " $>$ %d" % cfg.bins[idx]

def buildHist(samples, files, histpath, scale_factors):
    h = files[samples[0]].Get(histpath).Clone()
    for s in samples[1:]:
        tmp = files[s].Get(histpath)
        if s in scale_factors:
            tmp = tmp.Clone()
            tmp.Scale(scale_factors[s])
        h.Add(tmp)
    h.Scale(cfg.constants["lumi"]/cfg.constants["icf_default"])
    return h

def getFile(fname, fset, default_fset="zero"):
    fpath = fname % cfg.path[fset]
    if not os.path.exists(fpath):
        print "[WARNING] File: %s" % fname
        print "File not found for systematic '%s'. Using '%s' version instead!" % (fset, default_fset)
        fpath = fname % cfg.path[default_fset]
    if not os.path.exists(fpath): raise IOError("File not found: %s" % fname)
    return r.TFile(fpath)

def extract(fset, data, mc, scale_factors={}):
    tfiles = dict([(n, getFile(fname, fset, "zero")) for (n, fname) in cfg.files.iteritems()])

    data_signal = [buildHist(data, tfiles,
                             cfg.bin_fmt % (cfg.bin_name, b, "", cfg.hname), scale_factors)
                   for b in cfg.bins]
    data_control = [buildHist(data, tfiles,
                              cfg.bin_fmt % (cfg.bin_name, b, "_BKG", cfg.hname), scale_factors)
                    for b in cfg.bins]
    mc_signal = [buildHist(mc, tfiles,
                           cfg.bin_fmt % (cfg.bin_name, b, "", cfg.hname), scale_factors)
                 for b in cfg.bins]
    mc_control = [buildHist(mc, tfiles,
                            cfg.bin_fmt % (cfg.bin_name, b, "_BKG", cfg.hname), scale_factors)
                  for b in cfg.bins]

    return  [
        r.BinData(dsig, dcontrol, mcsig, mccontrol)
        for (dsig, dcontrol, mcsig, mccontrol)
        in zip(data_signal, data_control, mc_signal, mc_control)
        ]


def extractSignalEffs(fset, sample, bin_name, kfactors=None, asdict = False):
    tfiles = dict([(n, getFile(fname, fset, "zero"))
                   for (n, fname) in cfg.files.iteritems()])
    nocuts = tfiles[sample].Get("Counter_BSMGrid_NoCuts").Get("SUSYGrid")
    nocuts_noweight = tfiles[sample].Get("Counter_BSMGrid_NoCuts").Get("SUSYGrid_noweight")

    xs = nocuts.Clone()
    xs.Divide(nocuts_noweight)
    xs.Scale(cfg.constants["lumi"]/cfg.constants["icf_default"])

    sigbins = []
    for b in cfg.bins:
        sigbins.append(tfiles[sample].Get(cfg.bin_fmt % (cfg.bin_name, b, "", "SUSYGrid")))

    for sigbin in sigbins:
        sigbin.Divide(nocuts)
    if kfactors:
        processes, records = readKFactors(cfg.kfactor_files[kfactors])

    effs = []
    for xx in range(sigbins[0].GetNbinsX()+1):
        for yy in range(sigbins[0].GetNbinsY()+1):
            (x, y) = (int(sigbins[0].GetXaxis().GetBinUpEdge(xx)),
                      int(sigbins[0].GetYaxis().GetBinUpEdge(yy)))
            point = {"efficiencies": [],
                     "loxs" : xs.GetBinContent(xx,yy),
                     "m0" : x,
                     "m1/2" : y}
            for sigbin in sigbins:
                eff = sigbin.GetBinContent(xx,yy)
                point["efficiencies"].append(eff)
            if kfactors:
                if (x, y) in records:
                    rec = records[(x,y)]
                    point["nloxs"] = sum([float(rec[proc]) for proc in processes])
            effs.append(point)
    if asdict: effs = dict([((p["m0"], p["m1/2"]), p) for p in effs])
    return effs

def readKFactors(fname):
    header = None
    records = {}
    for line in open(fname):
        fields = line.split('|')
        pdict = {}

        if header is None:
            header = [f.strip().rstrip() for f in fields[1:-1]]
            continue

        point_fields = fields[1].split(",")

        if "(" in point_fields[0]:
            pfield = point_fields[0]
            bracket = pfield[pfield.find("(")+1:pfield.find(")")]
            point_fields[0] = pfield[pfield.find(")")+1:]
            point_fields.append(bracket)

        for pfield in point_fields:
            keyval = pfield.split("=")
            if len(keyval) == 2:
                pdict[keyval[0].strip().rstrip()] = keyval[1].strip().rstrip()
        for idx, f in enumerate(fields[2:-1]):
            pdict[header[idx+1]] = f.strip().rstrip()
        records[(int(pdict["m0"]), int(pdict["m1/2"]))] = pdict
    return header[1:], records

def pruneZeros(effs):
    return [k for k in effs if sum(k["efficiencies"]) > 0.05]

def rootkill(thing) :
    #free up memory (http://wlav.web.cern.ch/wlav/pyroot/memory.html)
    thing.IsA().Destructor( thing )

# Systematics
def jecSystematicBkg():
    return (extract("metup",   cfg.bkg_samples, cfg.bkg_samples),
            extract("metdown", cfg.bkg_samples, cfg.bkg_samples))
def metresSystematicBkg():
    one = extract("metres",    cfg.bkg_samples, cfg.bkg_samples)
    return (one, one)
def polSystematicBkg():
    return (extract("polup",   cfg.bkg_samples, cfg.bkg_samples),
            extract("poldown", cfg.bkg_samples, cfg.bkg_samples))
def lepSystematicBkg():
    one = extract("muscale",      cfg.bkg_samples, cfg.bkg_samples)
    return (one, one)
def WttSystematicBkg():
    return (extract("zero",    cfg.bkg_samples, cfg.bkg_samples,
                    {"tt":1.5, "w":0.7}),
            extract("zero",    cfg.bkg_samples, cfg.bkg_samples,
                    {"tt":0.5, "w":1.3}))

def getSystematicsBkg():
    syst_funcs = {
        "jec"    : jecSystematicBkg,
        "metres" : metresSystematicBkg,
        "pol"    : polSystematicBkg,
        "lep"    : lepSystematicBkg,
        "Wtt"    : WttSystematicBkg
        }
    out = []
    for syst in cfg.systInfo.keys():
        if syst in cfg.includeSysts: out += [(syst, syst_funcs[syst]())]
    return out

def getSystematicShiftsR(nom, up, down):
    def sign(a, b):
        if a >= b: return 1.0
        else: return -1.0
    def symmetriseSyst(a, b):
        return max(a, b)
    shift_up = [abs(up[idx].R() - b.R()) for idx, b in enumerate(nom)]
    shift_down = [abs(b.R() - down[idx].R()) for idx, b in enumerate(nom)]
    shift_sign = [sign(up[idx].R(), b.R()) for idx, b in enumerate(nom)]
    shifts = [ssign*symmetriseSyst(a, b)
              for a, b, ssign in zip(shift_up, shift_down, shift_sign)]
    return shifts

def getZeroMC():
    return extract("zero", cfg.bkg_samples, cfg.bkg_samples, cfg.bin_name)
def getZeroMCData():
    return extract("zero", cfg.data_samples, cfg.bkg_samples, cfg.bin_name)

def makePredictions(data):
    return [r.createBin(databin) for databin in data]

def addSystematic(name, data, results, syst):
    for idx, res in enumerate(results):
        r.addSystematic(name, res, data[idx], syst[0][idx], syst[1][idx])

def getAllSystematics():
    return [name for name, field in cfg.systInfo.iteritems()]

def getSignalSystematics():
    return [name for name, fields in cfg.systInfo.iteritems()
            if fields["signal"]]
def getBackgroundOnlySystematics():
    return list(set(getAllSystematics())
            - set(getSignalSystematics()))


def loadFile(fname):
    if fname.endswith(".json"):
        import json
        return json.load(open(fname))
    elif fname.endswith(".pkl"):
        import cPickle as pickle
        p = pickle.Unpickler(open(fname))
        res = p.load()
        del p
        return res

def saveFile(ob, fname):
    if fname.endswith(".json"):
        import json
        json.dump(ob, open(fname, "w"), indent = 0)
    elif fname.endswith(".pkl"):
        import cPickle as pickle
        p = pickle.Pickler(open(fname, "wb"))
        p.fast = True
        p.dump(ob)
