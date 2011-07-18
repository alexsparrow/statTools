# Configuration file

# SumLepPT (or PFMET bins)
bins = [250, 350, 450]

useRealData = True
icfNEventsIn = 10000.
icfDefaultLumi = 100.
lumiError   = 0.04         # Relative error on luminosity estimate (for limit setting)
minXSToConsider = 0.01

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
    "metres":"../resultsMC_metres_conservative",
    "polup":"../resultsMC_polup",
    "poldown":"../resultsMC_poldown",
    "muscale":"../resultsMC_muptscale"
    }

# Name format of the histogram path
bin_fmt = "Counter_BSMGrid_%s%d%s_scale1/%s"
# Name of the counter histogram for SM MC
hname = "SM_Events"
# Which susyScan to use
susyScan = "tanbeta10"
# use NLO signal xs for limit?
use_nloxs = False

processes = ["gg", "sb", "ss", "sg", "ll", "nn", "ng", "bb", "tb", "ns"]



# Benchmark points to use in limits plotting
lmPoints = [
    ("LM0", 200, 160),
    ("LM1", 60, 250),
    ("LM3", 330,240),
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
    "metres" : dict(zip(fields, ["metres", "MET Resolution Uncertainty", True,    True])),
    "lep"    : dict(zip(fields, ["lep",    "Lepton pT Scale",            True,    True])),
    "pol"    : dict(zip(fields, ["pol",    "W Polarisation",             False,   True])),
    "Wtt"    : dict(zip(fields, ["Wtt",    "W/tt Ratio",                 False,   True])),
}

plusMinus = {"OneSigma" : 1.0}

class Muon:
    name = "muon"
    # Integrated luminosity to use for limit setting/systs
    lumi = 1000.0
    # background MC to use in pseudo-data
    bkgSamples = ["w", "tt", "z"]
    # signal MC to use in pseudo-data
    sigSamples = ["lm1"]
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
        "w" : "%s/Muons_WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1.root",
        "tt" : "%s/Muons_WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1.root",
        "z" : "%s/Muons_DYJetsToLL_TuneZ2_M_50_7TeV_madgraph_tauola_Spring11_PU_S1_START311_V1G1_v1.root",
        "lm1" : "%s/Muons_LM1_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
        "lm3" : "%s/Muons_LM3_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
        "lm6" : "%s/Muons_LM6_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
        "tanbeta10" : "%s/Muons_PhysicsProcesses_mSUGRA_tanbeta10Fall10v1.root",
        "tanbeta10" : "%s/Muons_mSUGRA_m0_20to2000_m12_20to760_tanb_10andA0_0_7TeV_Pythia6Z_Summer11_PU_S4_START42_V11_FastSim_v1.root",
        "data42x" : "%s/../resultsData/Muons_data.root"
        }

    includeSignalSysts = [
        "jec",
    ]

    includeBackgroundSysts = [
        "jec",
        "metres",
        "Wtt"
    ]

    # Constants used in limit-setting


class Electron:
    name = "electron"
    # Integrated luminosity to use for limit setting/systs
    lumi = 1000.0
    # background MC to use in pseudo-data
    bkgSamples = ["w", "tt", "z"]
    # signal MC to use in pseudo-data
    sigSamples = ["lm1"]
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
        "w" : "%s/Electrons_WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1.root",
        "tt" : "%s/Electrons_WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v1.root",
        "z" : "%s/Electrons_DYJetsToLL_TuneZ2_M_50_7TeV_madgraph_tauola_Spring11_PU_S1_START311_V1G1_v1.root",
        "lm1" : "%s/Electrons_LM1_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
        "lm3" : "%s/Electrons_LM3_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
        "lm6" : "%s/Electrons_LM6_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
#        "tanbeta10" : "%s/Electrons_PhysicsProcesses_mSUGRA_tanbeta10Fall10v1.root",
        "tanbeta10" : "%s/Electrons_mSUGRA_m0_20to2000_m12_20to760_tanb_10andA0_0_7TeV_Pythia6Z_Summer11_PU_S4_START42_V11_FastSim_v1.root",
        "data42x" : "%s/../resultsData/Electrons_data.root"
        }

    includeSignalSysts = [
  #      "jec",
    ]

    includeBackgroundSysts = [
       # "jec",
       # "metres",
       # "Wtt"
    ]


channels = [Muon, Electron]






