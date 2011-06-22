#!/usr/bin/env python
import ROOT as r
import os
import math

def OneLeptonSimple( constants, data, backgroundInfo, signalInfo=None, systs=None):
    w = r. RooWorkspace("wspace")
    terms = []
    obs = []
    nuis = []
    model = None
    if systs:
        sig_systs = systs["signal"]
        bg_only_systs = systs["bg_only"]
        systs = sig_systs + bg_only_systs
    else:
        systs = bg_only_systs = sig_systs = []

    def wimport(item):
        # suppress info messages
        r.RooMsgService.instance().setGlobalKillBelow(r.RooFit.WARNING)
        getattr(w, "import")(item)
        #re-enable all messages
        r.RooMsgService.instance().setGlobalKillBelow(r.RooFit.DEBUG)

    def signalTerms():
        wimport(r.RooRealVar("f", "f", 0.1, 0.0, 2.0))
        wimport(r.RooRealVar("xs", "xs", signalInfo["xs"]))
        wimport(r.RooRealVar("lumi", "lumi", constants["lumi"]))
        wimport(r.RooRealVar("nuLumiMean", "nuLumiMean", 1.0))
        wimport(r.RooRealVar("nuLumi", "nuLumi", 1.0, 0.0, 2.0))
        wimport(r.RooRealVar("nuLumiDelta", "nuLumiDelta", 2*constants["lumiError"]))
        wimport(r.RooGaussian("nuLumiGauss", "nuLumiGauss", w.var("nuLumiMean"), w.var("nuLumi"), w.var("nuLumiDelta")))
        obs.append("nuLumiMean")
        nuis.append("nuLumi")
        terms.append("nuLumiGauss")

    def nuisanceParams():
        for syst in systs:
            if ("R%sShift" % syst in backgroundInfo or
                "eff%sShift" % syst in signalInfo):
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
        for idx, eff in enumerate(signalInfo["efficiencies"]):
            wimport(r.RooRealVar("bkgR%d" % idx, "bkgR%d" % idx, backgroundInfo["R"][idx]))
            wimport(r.RooRealVar("nuBkgNControl%d" % idx, "nuBkgNControl%d" % idx, 1, 0, 1))
            wimport(r.RooRealVar("nuBkgNControl%dMean" % idx, "nuBkgNControl%dMean" % idx, 1))
            wimport(r.RooRealVar("nuBkgNControl%dSigma" % idx, "nuBkgNControl%dSigma" % idx,
                                 math.sqrt(backgroundInfo["NControl"][idx])))
            wimport(r.RooRealVar("bkgNControl%d" % idx, "bkgNControl%d" % idx, backgroundInfo["NControl"][idx]))
            wimport(r.RooGaussian("bkgNControl%dGauss" % idx, "bkgNControl%dGauss" % idx,
                                  w.var("nuBkgNControl%d" % idx), w.var("nuBkgNControl%dMean" % idx),
                                  w.var("nuBkgNControl%dSigma" % idx)))
            terms.append("bkgNControl%dGauss" % idx)
            obs.append("nuBkgNControl%dMean" % idx)
            nuis.append("nuBkgNControl%d" % idx)
            R_systs = []
            for syst in bg_only_systs:
                if ("R%sShift" % syst) in backgroundInfo:
                    name = "bkgR%d%s" % (idx, syst)
                    wimport(r.RooRealVar("%sShift" % name, "%sShift" % name,
                                         backgroundInfo["R%sShift" % syst][idx]))
                    wimport(r.RooFormulaVar("%sScale" % name, "((@0) + (@1)*(@2))/(@3)",
                                            r.RooArgList(w.var("bkgR%d" % idx), w.var("%sShift" % name),
                                                         w.var("nu%s" % syst), w.var("bkgR%d" % idx))))
                    R_systs.append("%sScale" % name)

            R_terms = [w.var("bkgR%d" % idx), w.var("bkgNControl%d" % idx)]
            R_terms.extend([w.function(syst) for syst in R_systs])
            formula_str = "*".join(["(@%d)" % x for x in range(len(R_terms))])
            wimport(r.RooFormulaVar("bkgN%d" % idx, formula_str, r.RooArgList(*R_terms)))

    def signalBins():
        for idx, eff in enumerate(signalInfo["efficiencies"]):
            wimport(r.RooRealVar("signalEffNom%d" % idx, "signalEff%d" % idx, eff))
            signalEff_systs = []
            for syst in sig_systs:
                if "eff%sShift" % syst in signalInfo:
                    name = "signalEff%d%s" % (idx, syst)
                    wimport(r.RooRealVar(name+"Shift", name+"Shift" % idx,
                                         signalInfo["eff%sShift" % syst][idx]))
                    wimport(r.RooFormulaVar(name+"Scale" % idx, "((@0) + (@1)*(@2))/(@3)",
                                            r.RooArgList(w.var("signalEffNom%d" % idx), w.var("nu%s" % syst),
                                                         w.var(name+"Shift" % idx),
                                                         w.var("signalEffNom%d" % idx))))
                    signalEff_systs += [name+"Scale" % idx]

            signalEff_terms = [w.var("signalEffNom%d" % idx)]
            signalEff_terms.extend([w.function(syst) for syst in signalEff_systs])
            formula_str = "*".join(["(@%d)" % x for x in range(len(signalEff_terms))])
            wimport(r.RooFormulaVar("signalEff%d" % idx, formula_str, r.RooArgList(*signalEff_terms)))

            wimport(r.RooProduct("signalN%d" % idx, "signalS%d" % idx, r.RooArgSet(w.var("f"),
                                                                                   w.var("nuLumi"),
                                                                                   w.var("xs"),
                                                                                   w.var("lumi"),
                                                                                   w.function("signalEff%d" % idx))))
            wimport(r.RooAddition("expectedN%d" % idx, "expectedN%d" % idx, r.RooArgSet(w.function("bkgN%d" % idx),
                                                                                        w.function("signalN%d" % idx))))
            wimport(r.RooRealVar("observedN%d" % idx, "observedN%d" % idx, data["NObserved"][idx]))
            wimport(r.RooPoisson("poiss%d" % idx, "poiss%d" % idx, w.var("observedN%d" % idx), w.function("expectedN%d" % idx)))
            terms.append("poiss%d" % idx)
            obs.append("observedN%d" % idx)
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

