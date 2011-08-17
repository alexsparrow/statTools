# Configuration file
import math
# SumLepPT (or PFMET bins)
bins = [150, 250, 350, 450]

useRealData = True
icfNEventsIn = 10000.
icfDefaultLumi = 100.
lumiError   = 0.06         # Relative error on luminosity estimate (for limit setting)
minXSToConsider = 0.00001
minEffToConsider = 0.000001
lumiCorrection = 1.05
run_systematics = False
includeSignalContamination = True
clsToys = 1000

# Whether to do LP analysis
analysis = "lp"
# or pfmet
#analysis = "pfmet"

# Set the bin_name depending on analysis selected
# Used to locate correct histograms
if analysis == "lp": binName = "SumLepPT"
elif analysis == "pfmet" : binName = "PFMETCut"

# These are paths to various versions of the output ROOT files
# The zero entry corresponds to unscaled MC
# The others correspond to systematic variations
path = {
    "zero":"../resultsMC",
    "metup":"../resultsMC_metup",
    "metdown":"../resultsMC_metdown",
    "metup_flat" : "../resultsMC_metup_flat",
    "metdown_flat": "../resultsMC_metdown_flat",
    "metres":"../resultsMC_metres_conservative",
    "metres11":"../resultsMC_metres_11",
    "metres12":"../resultsMC_metres_12",
    "polup":"../resultsMC_polup",
    "poldown":"../resultsMC_poldown",
    "muscale":"../resultsMC_mupt",
    }

#if run_systematics: path = dict([(k,v+"_SYST") for k, v in path.iteritems()])

# Name format of the histogram path
bin_fmt = "Counter_BSMGrid_%s%d%s_scale1/%s"
# Name of the counter histogram for SM MC
hname = "SM_Events"
hname_noweight = "SM_Events_noweight"
# Which susyScan to use
susyScan = "tanbeta10"
# use NLO signal xs for limit?
use_nloxs = False

processes = ["gg", "sb", "ss", "sg", "ll", "nn", "ng", "bb", "tb", "ns"]

pdfUncertainty = 0.1

# Benchmark points to use in limits plotting
lmPoints = [
    ("LM0", 200, 160),
    ("LM1", 60, 250),
    ("LM2", 185, 350),
    ("LM3", 330,240),
    ("LM4", 210, 285),
  #  ("LM5", 230,    360),

    ("LM6", 85, 400)
    ]

# Defines systematics to be included in limit setting
systs = {
    "signal": ["jec", "metres", "lep"],
    "bg_only" : ["Wtt", "pol"]
    }

# List of systematics
fields =          [             "name",   "title",                      "signal", "background"]
systInfo =  {
    "jec" :    dict(zip(fields, ["jec",    "JES Uncertainty",            True,    True])),
    "jec_flat" :    dict(zip(fields, ["jec_flat",    "JES Uncertainty (Flat 5\%)",            True,    True])),

    "metres" : dict(zip(fields, ["metres", "MET Resolution Uncertainty", True,    True])),
    "metres11" : dict(zip(fields, ["metres11", "MET Resolution Uncertainty (11\%)", True,    True])),
    "metres12" : dict(zip(fields, ["metres12", "MET Resolution Uncertainty (12\%)", True,    True])),
    "lep"    : dict(zip(fields, ["lep",    "Lepton pT Scale",            True,    True])),
    "pol"    : dict(zip(fields, ["pol",    "W Polarisation",             False,   True])),
    "Wtt"    : dict(zip(fields, ["Wtt",    "W/tt Ratio",                 False,   True])),
    "MCStats" : dict(zip(fields, ["MCStats", "MC Statistics",            False,   True])),
    "pcdfunc" : dict(zip(fields, ["pdfunc", "PDF Uncertainty",            True, False]))
}

plusMinus = {"OneSigma" : 1.0}

class Muon:
    name = "muon"
    # Integrated luminosity to use for limit setting/systs
    lumi = 1082.0*lumiCorrection
    # Trigger efficiency
    triggerEfficiency = 0.91 if useRealData else 1.0
    # background MC to use in pseudo-data
    bkgSamples = ["w", "tt", "z"]
    # signal MC to use in pseudo-data
    sigSamples = []
    # MC PseudoData
    pseudoDataSamples = bkgSamples + sigSamples
    realDataSamples = ["data42x"]

    if useRealData:
        dataSamples = realDataSamples
        mcLumi = None
    else:
        dataSamples = pseudoDataSamples
        mcLumi = lumi
    # These give the paths for each MC sample according to their short name
    # The %s will be replaced with a base directory from the dictionary above
    files = {
#        "w" : "%s/Muons_WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1.root",
        "w" : "%s/Muons_WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1_v15_03_13.root",
        "tt" : "%s/Muons_TTJets_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1_V15_03_14.root",
        "z" : "%s/Muons_DYJetsToLL_TuneZ2_M_50_7TeV_madgraph_tauola_Spring11_PU_S1_START311_V1G1_v1.root",
        # "lm1" : "%s/Muons_LM1_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
        # "lm3" : "%s/Muons_LM3_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
        # "lm6" : "%s/Muons_LM6_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
        "tanbeta10" : "%s/Muons_mSUGRA_m0_20to2000_m12_20to760_tanb_10andA0_0_7TeV_Pythia6Z_Summer11_PU_S4_START42_V11_FastSim_v1.root",
        "data42x" : "%s/../resultsData/Muons_data.root"
        }

    if run_systematics:
        del files["tanbeta10"]
        del files["data42x"]
        # files["w"] =  "%s/Muons_WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1_v15_03_13.root"

    includeSignalSysts = [
        "jec",
        "metres",
        "pdfunc"
    ]

    includeBackgroundSysts = [
       "jec",
       "metres",
       "Wtt",
       "pol",
       "lep"
    ]

    # Constants used in limit-setting
    bkgPrediction = None
    ctrlChannel = None

class Electron:
    name = "electron"
    # Integrated luminosity to use for limit setting/systs
    lumi = 1079.0*lumiCorrection
    # Trigger efficiency
    triggerEfficiency = 0.96 if useRealData else 1.0

    # background MC to use in pseudo-data
    bkgSamples = ["w", "tt", "z"]
    # signal MC to use in pseudo-data
    sigSamples = []
    # MC PseudoData
    pseudoDataSamples = bkgSamples + sigSamples
    realDataSamples = ["data42x"]

    if useRealData:
        dataSamples = realDataSamples
        mcLumi = None
    else:
        dataSamples = pseudoDataSamples
        mcLumi = lumi


    # These give the paths for each MC sample according to their short name
    # The %s will be replaced with a base directory from the dictionary above
    files = {
        #        "w" : "%s/Electrons_WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1.root",
        "w" : "%s/Electrons_WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1_v15_03_13.root",
        "tt" : "%s/Electrons_TTJets_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1.root",
        "z" : "%s/Electrons_DYJetsToLL_TuneZ2_M_50_7TeV_madgraph_tauola_Spring11_PU_S1_START311_V1G1_v1.root",
        # "lm1" : "%s/Electrons_LM1_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
        # "lm3" : "%s/Electrons_LM3_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
        # "lm6" : "%s/Electrons_LM6_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
        #        "tanbeta10" : "%s/Electrons_PhysicsProcesses_mSUGRA_tanbeta10Fall10v1.root",
        "tanbeta10" : "%s/Electrons_mSUGRA_m0_20to2000_m12_20to760_tanb_10andA0_0_7TeV_Pythia6Z_Summer11_PU_S4_START42_V11_FastSim_v1.root",
        "data42x" : "%s/../resultsData/Electrons_data.root"
        }

    if run_systematics:
        del files["tanbeta10"]
        del files["data42x"]

    includeSignalSysts = [
       "jec",
       "metres",
       "pdfunc"
    ]

    includeBackgroundSysts = [
        "jec",
        "metres",
        "Wtt",
        "pol"
    ]

    # Old numbers without residual corrections applied
    # ewkN   = [292, 94, 21, 11]
    # ewkErr = [23,  12, 5,  4 ]
    ewkN   = [329.4, 117.6, 25.9, 12.4]
    #    ewkErr = [22.7,  11.6, 5.8,  3.8 ]
    ewkErrStat = [0.05, 0.09, 0.16, 0.24]
    ewkErrMCStat = [0.09, 0.16, 0.25, 0.32]
    ewkErr = [math.sqrt(a**2 + b**2)*c for a, b, c in zip(ewkErrStat, ewkErrMCStat, ewkN)]
    ctrlChannel = Muon

    if not useRealData: bkgPrediction = None
    else: bkgPrediction = "QCDFit" # "OtherChannel", None

channels = [Muon, Electron]






