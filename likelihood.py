#!/usr/bin/env python
import ROOT as r
import os
import math

class Channel(object):
    def __init__(self, name, lumi, NObserved, NControl, R, signalEff):
        self.name = name
        self.lumi = lumi
        self.NObserved = NObserved
        self.NControl = NControl
        self.R = R["nominal"]
        self.RSyst = dict([(k,v) for k, v in R.iteritems() if k != "nominal"])
        self.signalEff = signalEff["nominal"]
        self.signalEffSyst = dict([(k, v) for k, v in signalEff.iteritems() if k != "nominal"])
        self.NControlError = [math.sqrt(nc) for nc in self.NControl]


    def signalSystematics(self):
        return set(self.signalEffSyst.keys())
    def backgroundSystematics(self):
        return set(self.RSyst.keys())
    def allSystematics(self):
        return self.signalSystematics() | self.backgroundSystematics()
    def enumBins(self):
        return enumerate(self.signalEff)

def OneLeptonSimple(globals, *channels):
    w = r. RooWorkspace("wspace")
    model = None
    obs = [ ]
    terms = [ ]
    nuis = [ ]
    def wimport(*items):
        for item in items:
            # suppress info messages
            r.RooMsgService.instance().setGlobalKillBelow(r.RooFit.WARNING)
            getattr(w, "import")(item)
            #re-enable all messages
            r.RooMsgService.instance().setGlobalKillBelow(r.RooFit.DEBUG)

    def signalTerms():
        wimport(r.RooRealVar("f", "f", 0.1, 0.0, 2.0)) # f was 0.1 . upper was 2.0
        print "xs = %.2f" % globals["xs"]
        wimport(r.RooRealVar("xs", "xs", globals["xs"]))
        wimport(r.RooRealVar("nuLumiMean", "nuLumiMean", 1.0))
        wimport(r.RooRealVar("nuLumi", "nuLumi", 1.0, 0.0, 2.0))
        wimport(r.RooRealVar("nuLumiDelta", "nuLumiDelta", 2*globals["lumiError"]))
        wimport(r.RooGaussian("nuLumiGauss", "nuLumiGauss", w.var("nuLumiMean"),
                              w.var("nuLumi"), w.var("nuLumiDelta")))
        obs.append("nuLumiMean")
        terms.append("nuLumiGauss")
        nuis.append("nuLumi")
        for ch in channels:
            print "Lumi %s = %.2f" % (ch.name, ch.lumi)
            wimport(r.RooRealVar("%sLumi" % ch.name, "%sLumi" % ch.name, ch.lumi))

    def nuisanceParams():
        systs = set.union(*[ch.allSystematics() for ch in channels])
        for syst in systs:
            name = "nu%s" % syst
            wimport(r.RooRealVar(name, name, 0, -5, 5))
            wimport(r.RooRealVar(name+"Mean", name+"Mean", 0))
            wimport(r.RooRealVar(name+"Sigma", name+"Sigma", 1.0))
            wimport(r.RooGaussian(name+"Gauss", name+"Gauss",
                                  w.var(name), w.var(name+"Mean"),
                                  w.var(name+"Sigma")))
            nuis.append(name)
            terms.append(name+"Gauss")
            obs.append(name+"Mean")

    def backgroundPredictions():
        for ch in channels:
            for idx, eff in ch.enumBins():
                prefix = "%sBkg%d" % (ch.name, idx)
                wimport(r.RooRealVar("%s_RNom" % prefix, "%s_RNom" % prefix, ch.R[idx]))
                wimport(r.RooRealVar("%s_NControl" % prefix, "%s_NControl" % prefix, ch.NControl[idx]))
                prefix = "nu%sBkg%dNControl" % (ch.name, idx)
                wimport(r.RooRealVar(prefix, prefix, 1, 0, 1))
                wimport(r.RooRealVar("%sMean" % prefix, "%sMean" % prefix, 1))
                wimport(r.RooRealVar("%sSigma" % prefix, "%sSigma" % prefix, ch.NControlError[idx]))
                wimport(r.RooGaussian("%sGauss" % prefix, "%sGauss" % prefix,
                                      w.var(prefix), w.var("%sMean" % prefix), w.var("%sSigma" % prefix)))
                terms.append("%sGauss" % prefix)
                obs.append("%sMean" % prefix)
                nuis.append(prefix)
                R_systs = []
                for syst in ch.backgroundSystematics():
                    name = "%sBkg%d_R%s" % (ch.name, idx, syst)
                    wimport(r.RooRealVar("%sShift" %  name, "%sShift" % name, ch.RSyst[syst][idx]))
                    wimport(r.RooFormulaVar("%sScale" % name, "((@0) + (@1)*(@2))/(@3)",
                                            r.RooArgList(w.var("%sBkg%d_RNom" % (ch.name, idx)),
                                                               w.var("%sShift" % name),
                                                               w.var("nu%s" % syst),
                                                               w.var("%sBkg%d_RNom" % (ch.name, idx)))))
                    R_systs.append("%sScale" % name)

                R_terms = [w.var("%sBkg%d_RNom" % (ch.name, idx)), w.var("%sBkg%d_NControl" % (ch.name, idx))]
                R_terms.extend([w.function(syst) for syst in R_systs])
                formula_str = "*".join(["(@%d)" % x for x in range(len(R_terms))])
                wimport(r.RooFormulaVar("%sBkg%d_N" % (ch.name, idx), formula_str, r.RooArgList(*R_terms)))

    def signalBins():
        for ch in channels:
            for idx, eff in ch.enumBins():
                wimport(r.RooRealVar("%sSignal%d_EffNom" % (ch.name, idx), "%sSignal%d_Eff" % (ch.name, idx), ch.signalEff[idx]))
                signalEff_systs = []
                for syst in ch.signalSystematics():
                    name = "%sSignal%d_Eff%s" % (ch.name, idx, syst)
                    wimport(r.RooRealVar(name+"Shift", name+"Shift",
                                         ch.signalEffSyst[syst][idx]))
                    wimport(r.RooFormulaVar(name+"Scale", "((@0) + (@1)*(@2))/(@3)",
                                            r.RooArgList(w.var("%sSignal%d_EffNom" % (ch.name, idx)), w.var("nu%s" % syst),
                                                         w.var(name+"Shift"),
                                                         w.var("%sSignal%d_EffNom" % (ch.name, idx)))))
                    signalEff_systs += [name+"Scale"]

                signalEff_terms = [w.var("%sSignal%d_EffNom" % (ch.name, idx))]
                signalEff_terms.extend([w.function(syst) for syst in signalEff_systs])
                formula_str = "*".join(["(@%d)" % x for x in range(len(signalEff_terms))])
                wimport(r.RooFormulaVar("%sSignal%d_Eff" % (ch.name, idx), formula_str, r.RooArgList(*signalEff_terms)))

                wimport(r.RooProduct("%sSignal%d_N" % (ch.name, idx), "%sSignal%d_N" % (ch.name, idx),
                                     r.RooArgSet(w.var("f"), w.var("nuLumi"), w.var("xs"), w.var("%sLumi" % ch.name),
                                                 w.function("%sSignal%d_Eff" % (ch.name, idx)))))
                wimport(r.RooAddition("%sExpected%d_N" % (ch.name, idx), "%sExpected%d_N" % (ch.name, idx),
                                      r.RooArgSet(w.function("%sBkg%d_N" % (ch.name, idx)), w.function("%sSignal%d_N" % (ch.name, idx)))))
                print "%s - Observed" % ch.name, ch.NObserved[idx]
                wimport(r.RooRealVar("%sObserved%d_N" % (ch.name, idx), "%sObserved%d_N" % (ch.name, idx), ch.NObserved[idx]))
                wimport(r.RooPoisson("%sPoiss%d" % (ch.name, idx), "%sPoiss%d" % (ch.name, idx),
                                     w.var("%sObserved%d_N" % (ch.name, idx)), w.function("%sExpected%d_N" % (ch.name, idx))))
                terms.append("%sPoiss%d" % (ch.name, idx))
                obs.append("%sObserved%d_N" % (ch.name, idx))

    def model():
        w.factory("PROD:model(%s)" % ",".join(terms))

    signalTerms()
    nuisanceParams()
    backgroundPredictions()
    signalBins()
    model()
    w.defineSet("obs", ",".join(obs))
    w.defineSet("nuis", ",".join(nuis))
    modelConfig = r.RooStats.ModelConfig("modelConfig", w)
    modelConfig.SetPdf("model")
    w.defineSet("poi", "f")
    modelConfig.SetParametersOfInterest(w.set("poi"))
    modelConfig.SetNuisanceParameters(w.set("nuis"))


    data = r.RooDataSet("dataName", "dataTitle", w.set("obs"))
    data.add(w.set("obs"))
    return (w, modelConfig, data)

