#!/usr/bin/env python
import ROOT as r
import json, math, array, os

from config import lmPoints, Muon
import utils

files = [
    # ("limit_data", "limit500pbdata.pkl"),
    # ("limit_mc", "limit_mc.pkl"),
    ("limit_nlo", "limit_nlo.pkl"),
    ("limit_lm1", "limit_lm1.pkl"),
    ("new", "limit_eles_mc_lm1_new.pkl"),
    ("limit_data", "limit_data_new.pkl")
    ]

nogc = []

def drawBenchmarkPoints():
    pts = []
    for p in lmPoints:
        pt = r.TMarker()
        pt.SetMarkerStyle(21)
        pt.SetMarkerSize(1.3)
        pt.DrawMarker(p[1], p[2])
        l = r.TLatex()
        l.DrawLatex(p[1]+20, p[2], p[0])

def plot2d(hist, name, draw_opt="colz",dir=None, log=False):
    c = r.TCanvas("brun")
    if log: c.SetLogz()
    c.SetGrid()
    r.gStyle.SetPalette(1)
    r.gROOT.SetStyle("Plain")
    hist.SetStats(r.kFALSE)
    hist.Draw(draw_opt)
    pts = drawBenchmarkPoints()
    if dir: path = "limit/%s" % dir
    else: path = "limit"
    try: os.makedirs(path)
    except: pass
    c.SaveAs("%s/%s.pdf" % (path, name))


def plotContours(conts, name, dir=None):
    # Plot 1 sigma contours
    c = r.TCanvas("brun")
    c.SetGrid()
    leg = makeLegend()
    line_cols = [r.kRed, r.kBlue, r.kGreen, r.kBlack]
    sorted_conts = sorted(conts, key = lambda x : r.TMath.MaxElement(x[1].GetN(),x[1].GetY()), reverse=True)

    for idx, (n, cont) in enumerate(sorted_conts):
        cont.SetLineColor(line_cols[idx])
        if idx == 0 : cont.Draw("AC")
        else: cont.Draw("C same")
    for n, cont in conts:
        leg.AddEntry(cont, n, "L")
    drawBenchmarkPoints()
    leg.Draw()
    if dir: path = "limit/%s" % dir
    else: path = "limit"
    try: os.makedirs(path)
    except: pass
    c.SaveAs("%s/%s.pdf" % (path, name))

def contour(h2d):
    h2d = h2d.Clone()
    g = r.TGraph(h2d.GetNbinsX())
    for hbin in range(1, h2d.GetNbinsX()):
        vals = [i for i in range(h2d.GetNbinsY()) if h2d.GetBinContent(hbin, i) > 0]
        vals.sort()
        vals.reverse()
        maxval = 0
        for v in vals:
            if v-1 in vals:
                maxval = v
                break
        g.SetPoint(hbin, 0.5*(h2d.GetXaxis().GetBinLowEdge(hbin) + h2d.GetXaxis().GetBinUpEdge(hbin)),
                   0.5*(h2d.GetYaxis().GetBinLowEdge(maxval) + h2d.GetYaxis().GetBinUpEdge(maxval)))
    gs = r.TGraphSmooth()
    g = gs.SmoothSuper(g)
    nogc.append(gs)
    return g

def makeLegend():
    return r.TLegend(0.7, 0.9, 0.9, 0.6)

class AutoHist:
    def __init__(self):
        self.hists = {}
        self.opts = {}

    def createHist(self, name, title, *args):
        if len(args) == 3: return r.TH1D(name, title, *args)
        elif len(args) == 6: return r.TH2D(name, title, *args)

    def fill(self, name, title, bin_ranges, values, **kwargs):
        if not name in self.hists:
            self.hists[name] = self.createHist(name, title, *bin_ranges)
            self.opts[name] = kwargs
        self.hists[name].Fill(*values)

    def setcontent(self, name, title, bin_ranges, values, **kwargs):
        if not name in self.hists:
            self.hists[name] = self.createHist(name, title, *bin_ranges)
            self.opts[name] = kwargs
        self.hists[name].SetBinContent(*values)


def extractHists(d):
    out = {}
    lumiString = "%d/pb;m_{0};m_{1/2}" % Muon.lumi
    hist_opts = (int(max_m0)/10, 0, max_m0, int(max_m12)/10, 0, max_m12)
    auto = AutoHist()

    for idx, p in enumerate(d["results"]):
        (x, y) = int(p["channels"][0]["m0"])/10, int(p["channels"][0]["m1/2"])/10
        auto.setcontent("hCrossSectionLO", "Cross Section (LO)", hist_opts, (x, y, p["channels"][0]["loxs"]), log=True)
        if "nloxs" in p["channels"][0]:
            auto.setcontent("hCrossSectionNLO", "Cross Section (NLO)", hist_opts, (x, y, p["channels"][0]["nloxs"]))
        for k in ["pl", "clsviatoys"]:
            if k in p["results"]:
                (x, y) = int(p["channels"][0]["m0"])/10, int(p["channels"][0]["m1/2"])/10
                if k == "pl": ul = p["results"]["pl"]["limit"]["high"]
                elif k == "clsviatoys":  ul = p["results"]["clsviatoys"]["limit"]["CLs"]
                auto.setcontent("hLimit_%s" % k, "Limit %s" % lumiString, hist_opts, (x, y, ul))
                for syst in utils.getAllSystematics():
                    if syst in p["results"][k]:
                        auto.setcontent("nu%s" % syst, "Nuisance %s" % syst, hist_opts,
                                        (x, y, p["results"]["pl"][syst]))
                print ul
                if ul <= 1:
                    auto.setcontent("hExcluded_%s" % k, "Excluded %s" % lumiString,
                                    hist_opts, (x, y, 1))

        if "quantiles" in p:
            for k, v in p["quantiles"].iteritems():
                name = "quantile_%s_limit" % k
                if not name in out:
                    out[name] = r.TH2D(k+"_limit", k, *hist_opts)
                out[name].SetBinContent(x, y, v)
                name = "quantile_%s_excluded" % k
                if v <= 1:
                    if not name in out:
                        out[name] = r.TH2D(k+"_excluded", k, *hist_opts)
                    out[name].SetBinContent(x, y, 1)
    return auto

if __name__ == "__main__":
    r.gROOT.SetBatch(True)
    rootf = r.TFile("limit.root", "recreate")

    overlay_contours = []
    for lname, fname in files:
        print "Reading file: %s" % fname
        j = utils.loadFile(fname)
        print "Done."
        max_m0 = max(p["m0"] for p in j["results"])
        max_m12 = max(p["m1/2"] for p in j["results"])
        print "Found %d" % len(j["results"])
        d = rootf.mkdir(lname)
        d.cd()
        h = extractHists(j)
        for k, v in h.hists.iteritems():
            plot2d(v, k, dir=lname, **h.opts[k])

        obs_contour = contour(h.hists["hExcluded_pl"])
#        overlay_contours += [(lname, obs_contour)]
        conts = [("observed", obs_contour)]
        for name, hist in h.hists.iteritems():
            if not name.startswith("quantile"): continue
            plot2d(hist, name, dir=lname, **h.opts[name])
            if name.endswith("excluded"):
                conts += [(name.split("_")[1], contour(hist))]
            if name == "quantile_Median_excluded":
                overlay_contours += [(lname, contour(hist))]
        plotContours(conts, "sigma_contours", dir=lname)
        del j
        del h
        del conts

    d = rootf.mkdir("overlay")
    d.cd()
    plotContours(overlay_contours, "overlayed")
    rootf.Write()
