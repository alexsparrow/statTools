import ROOT as r
import utils
import math, array

def rooFitResults(pdf, data, options = (r.RooFit.Verbose(False), r.RooFit.PrintLevel(-1), r.RooFit.Save(True))) :
    return pdf.fitTo(data, *options)

def plInterval(w, modelConfig, dataset, cl=0.95, poi="f"):
     calc = r.RooStats.ProfileLikelihoodCalculator(dataset, modelConfig)
     calc.SetConfidenceLevel(0.95)
     interval = calc.GetInterval()
     (low, high) = (interval.LowerLimit(w.var(poi)), interval.UpperLimit(w.var(poi)))
     utils.rootkill(interval)
     return (low, high)

def pseudoData(w, n):
    dataset = w.pdf("model").generate(w.set("obs"), n)
    out = []
    for i in range(int(dataset.sumEntries())):
        argset = dataset.get(i)
        data = r.RooDataSet("pseudoData%d" % i, "title", argset)
        data.add(argset)
        out.append(data)
    return out

def toys(w, modelConfig, dataset, nToys, cl=0.95):
    w.var("f").setVal(0.0)
    w.var("f").setConstant(True)
    results = rooFitResults(w.pdf("model"), dataset)

    pseudo = pseudoData(w, nToys)

    w.var("f").setVal(1.0)
    w.var("f").setConstant(False)

    w.saveSnapshot("snap", w.allVars())

    for i, dataset in enumerate(pseudo):
        w.loadSnapshot("snap")
        yield w, dataset

def capture(w, modelConfig, dataset, cl):
    out = {}
    out["limit"] = plInterval(w, modelConfig, dataset, cl)
    for syst in utils.getAllSystematics():
        try: out["%s" % syst] = w.var("nu%s" % syst).getVal()
        except ReferenceError: out["%s" % syst] = -1
    return out


def quantiles(limits, plusMinus):
    def histoFromList(l, name, title, bins) :
        h = r.TH1D(name, title, *bins)
        for item in l : h.Fill(item)
        return h
    def probList(plusMinus) :
        def lo(nSigma) : return ( 1.0-r.TMath.Erf(nSigma/math.sqrt(2.0)) )/2.0
        def hi(nSigma) : return 1.0-lo(nSigma)
        out = []
        out.append( (0.5, "Median") )
        for key,n in plusMinus.iteritems() :
            out.append( (lo(n), "MedianMinus%s"%key) )
            out.append( (hi(n), "MedianPlus%s"%key)  )
        return sorted(out)
    fst = lambda x : x[0]
    snd = lambda x : x[1]
    pl = probList(plusMinus)
    probs = map(fst, pl)
    names = map(snd, pl)
    probSum = array.array('d', probs)
    q = array.array('d', [0.0]*len(probSum))
    probSum = array.array('d', probs)
    q = array.array('d', [0.0]*len(probSum))

    h = histoFromList(limits, name = "upperLimit", title = ";upper limit on XS factor;toys / bin",
                      bins = (50, 1, -1)) #enable auto-range
    h.GetQuantiles(len(probSum), q, probSum)
    return dict(zip(names, q))
