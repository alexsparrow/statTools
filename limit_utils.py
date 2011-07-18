import ROOT as r
import utils
import math, array

def rooFitResults(pdf, data, options = (r.RooFit.Verbose(False), r.RooFit.PrintLevel(-1), r.RooFit.Save(True))) :
    return pdf.fitTo(data, *options)

def plInterval(w, modelConfig, dataset, cl=0.95, poi="f", plot=False):
    out = {}
    calc = r.RooStats.ProfileLikelihoodCalculator(dataset, modelConfig)
    w.var("f").setVal(0.1) # was 0.1
    w.var("f").setConstant(False)

    calc.SetConfidenceLevel(0.95)
    interval = calc.GetInterval()
    out["low"] = interval.LowerLimit(w.var(poi))
    out["high"] = interval.UpperLimit(w.var(poi))

    if plot:
        canvas = r.TCanvas("pl")
        canvas.SetTickx()
        canvas.SetTicky()
        plPlot = r.RooStats.LikelihoodIntervalPlot(interval)
        plPlot.Draw()
        canvas.Write()
    utils.rootkill(interval)
    return out

def cls(w, modelConfig, dataset, method, nToys, plot=False):
    def indexFraction(item, l):
        totalList = sorted(l+[item])
        return totalList.index(item)/(0.0+len(totalList))

    def histToList(name, title, nbins, l):
        hist = r.TH1D(name, title, nbins, min(l), max(l))
        for item in l: hist.Fill(item)
        return hist

    def pValue(w, nToys, plot_name=None):
        results = rooFitResults(w.pdf("model"), dataset)
        w.saveSnapshot("snap", w.allVars())
        maxData = -results.minNll()
        maxs = []
        graph = r.TGraph()
        for i,dset in enumerate(pseudoData(w, nToys)):
            w.loadSnapshot("snap")
            results = rooFitResults(w.pdf("model"), dset)
            maxs.append(-results.minNll())
            graph.SetPoint(i, i, indexFraction(maxData, maxs))
            utils.rootkill(results)
        if plot:
            c = r.TCanvas(plot_name)
            graph.Draw("a*")
            c.Write()
            hist = histToList("%s_hist" % plot_name, "", 50, maxs)
            hist_actual = histToList("%s_hist_actual" % plot_name, "", 50, [0, maxData])
            hist.Write()
            hist_actual.Write()
        utils.rootkill(graph)
        return indexFraction(maxData, maxs)

    out = {}

    if method == "Toys":
        w.var("f").setVal(0.0)
        w.var("f").setConstant()
        out["CLb"] = 1.0 - pValue(w, nToys, "CLb")
        w.var("f").setVal(1.0)
        w.var("f").setConstant()
        out["CLs+b"] = pValue(w, nToys, "CLs+b")

    out["CLs"] = out["CLs+b"]/out["CLb"] if out["CLb"] else 9.9
    return out

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

def capture(w, modelConfig, dataset, cl, method, globals):
    out = {}
    if method == "pl":
        pl_plot_name = "pl_%(m0)d_%(m1/2)d" % globals
        out["limit"] = plInterval(w, modelConfig, dataset, cl)
        for syst in utils.getAllSystematics():
            try: out["%s" % syst] = w.var("nu%s" % syst).getVal()
            except ReferenceError: out["%s" % syst] = -1
    elif method == "clsviatoys":
        out["limit"] = cls(w, modelConfig, dataset, "Toys", 1000)
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
