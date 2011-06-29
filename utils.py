import ROOT as r
import config as cfg
import os.path

def formatBin(idx):
    """ Return a human readable bin name """
    if idx < len(cfg.bins) -1:
        return "%d - %d" % (cfg.bins[idx], cfg.bins[idx+1])
    else:
        return " $>$ %d" % cfg.bins[idx]

def buildHist(samples, files, histpath, scale_factors):
    """ Loop through sample list 'samples' and fetch histogram at 'histpath'
    from TFile dictionary 'files'. Optionally look up scale factor from
    'scale_factors' and scale histogram appropriately.
    """
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
    """ Lookup a given filename 'fname', replacing %s in the string with the
    path to file set 'fset'. If the file can't be found, fall back to the one
    available in 'default_fset'.
    """
    fpath = fname % cfg.path[fset]
    if not os.path.exists(fpath):
        print "[WARNING] File: %s" % fname
        print "File not found for systematic '%s'. Using '%s' version instead!" % (fset, default_fset)
        fpath = fname % cfg.path[default_fset]
    if not os.path.exists(fpath): raise IOError("File not found: %s" % fname)
    return r.TFile(fpath)

def extract(fset, data, mc, scale_factors={}):
    """For the specified data samples 'data' and mc samples 'mc', extract signal
    and control histograms for the set of files 'fset'. Construct BinData
    objects (see predict.C) from these. Optionally scale histograms according to
    'scale_factors' dictionary.
    """
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


def extractSignalEffs(fset, sample, kfactors=None, asdict = False):
    """ Extract SUSY signal efficiencies per bin and output each mSUGRA point as a list
    'fset' : set of files to use
    'sample' : which sample e.g. tanbeta10
    'kfactors' : user K-factors for NLO xsection calculation
    'asdict' : Output a dictionary indexed by (m0, m1/2) instead
    """

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
    """ Parse k-factors text file in fname and return dictionary keyed by (m0,
    m1/2)"""
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

def rootkill(thing) :
    """ Delete a ROOT object. Needed to avoid memory leaks """
    #free up memory (http://wlav.web.cern.ch/wlav/pyroot/memory.html)
    thing.IsA().Destructor( thing )

# Background Systematics
# These functions return the background signal and control yields as BinData
# objects for each systematic variation (i.e. jec, met resolution etc.)
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
    """ Return all background systematics filtered by the includeBackgroundSysts
    list"""
    syst_funcs = {
        "jec"    : jecSystematicBkg,
        "metres" : metresSystematicBkg,
        "pol"    : polSystematicBkg,
        "lep"    : lepSystematicBkg,
        "Wtt"    : WttSystematicBkg
        }
    out = []
    for syst in cfg.systInfo.keys():
        if syst in cfg.includeBackgroundSysts: out += [(syst, syst_funcs[syst]())]
    return out

# Signal Systematics

def jecSystematicSignalEff():
    return (extractSignalEffs("metup", cfg.susyScan, cfg.susyScan, asdict=True),
            extractSignalEffs("metdown", cfg.susyScan, cfg.susyScan, asdict=True))
def metresSystematicSignalEff():
    one = extractSignalEffs("metres", cfg.susyScan, cfg.susyScan, asdict=True)
    return (one, one)
def lepSystematicSignalEff():
    one = extract("muscale", cfg.susyScan, cfg.susyScan, asdict=True)
    return (one, one)

def getSystematicsSignalEff():
    syst_funcs = {
        "jec" : jecSystematicSignalEff,
        "metres" : metresSystematicSignalEff,
        "lep" : lepSystematicSignalEff
        }
    out = []
    for syst in cfg.systInfo.keys():
        if syst in cfg.includeSignalSysts and syst in syst_funcs: out += [(syst, syst_funcs[syst]())]
    return out

# General functions for dealing with systematics
def calcSyst(nom, up, down):
    """ Return the largest shift (and appropriate sign) per bin from the nominal
    data to the up and down scaled data."""
    def sign(a, b):
        if a >= b: return 1.0
        else: return -1.0
    def symmetriseSyst(a, b):
        return max(a, b)

    shift_up = [abs(u - n) for u, n in zip(up, nom)]
    shift_down = [abs(d - n) for d, n in zip(down, nom)]
    shift_sign = [sign(u, n) for u, n in zip(up, nom)]
    shifts = [ssign*symmetriseSyst(u, d) for u, d, ssign in
              zip(shift_up, shift_down, shift_sign)]
    return shifts

def getSystematicShiftsEff(p, up, down):
    """ Calculate signal efficiency systematics.  p is a single mSUGRA
    point. up, down are dictionaries (keyed with m0,m1/2) for the up and down
    scaled SUSY points.
    """
    out = []
    (m0, m12) = (p["m0"], p["m1/2"])
    if not (m0, m12) in up or not (m0, m12) in down:
        return None
    up_eff = up[(m0, m12)]["efficiencies"]
    down_eff = down[(m0, m12)]["efficiencies"]
    return calcSyst(p["efficiencies"], up_eff, down_eff)


def getSystematicShiftsR(nom, up, down):
    """ Get systematic shift on R (Nsignal/Ncontrol) per bin"""
    nom = map(lambda x : x.R(), nom)
    up = map(lambda x: x.R(), up)
    down = map(lambda x : x.R(), down)
    return calcSyst(nom, up, down)


def getZeroMC():
    """ Return background only MC without systematic variation """
    return extract("zero", cfg.bkg_samples, cfg.bkg_samples, cfg.bin_name)
def getZeroMCData():
    """ Return MC pseudodata (possibly containing signal) without syst variation"""
    return extract("zero", cfg.data_samples, cfg.bkg_samples, cfg.bin_name)
def getZeroMCSignal():
    """ Return mSUGRA efficiencies without systematic variation"""
    return extractSignalEffs("zero", cfg.susyScan, cfg.susyScan)

def makePredictions(data):
    """ Turn BinData objects into BinResult representing prediction """
    return [r.createBin(databin) for databin in data]

def addSystematic(name, data, results, syst):
    """ Add systematic contribution to bins """
    for idx, res in enumerate(results):
        r.addSystematic(name, res, data[idx], syst[0][idx], syst[1][idx])

def getSignalSystematics():
    """ Return systematics affecting signal expectation """
    return [name for name, fields in cfg.systInfo.iteritems()
            if fields["signal"] and name in cfg.includeSignalSysts]

def getBackgroundSystematics():
    """ Return systematics affecting background prediction """
    return [name for name, fields in cfg.systInfo.iteritems()
            if fields["background"] and name in cfg.includeBackgroundSysts]

def getAllSystematics():
    """ Return all systematics """
    return set(getSignalSystematics()) | set(getBackgroundSystematics())


def loadFile(fname):
    """ Generic load file. json/picle depending on extension."""
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
    """ Generic save file. json/picle depending on extension."""
    if fname.endswith(".json"):
        import json
        json.dump(ob, open(fname, "w"), indent = 0)
    elif fname.endswith(".pkl"):
        import cPickle as pickle
        p = pickle.Pickler(open(fname, "wb"))
        # Needed to avoid bad_alloc
        p.fast = True
        p.dump(ob)
