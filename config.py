
# Configuration file

# SumLepPT (or PFMET bins)
bins = [150, 250, 350, 450]
# Whether to do LP analysis
analysis = "lp"
# or pfmet
#analysis = "pfmet"

# Set the bin_name depending on analysis selected
# Used to locate correct histograms
if analysis == "lp": bin_name = "SumLepPT"
elif analysis == "pfmet" : bin_name = "PFMETCut"

# background MC to use in pseudo-data
bkg_samples = ["w", "tt", "z"]
# signal MC to use in pseudo-data
sig_samples = []
data_samples = bkg_samples + sig_samples

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

# These give the paths for each MC sample according to their short name
# The %s will be replaced with a base directory from the dictionary above
files = {
#    "w" : "%s/default_Muons_WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Spring11_PU_S1_START311_V1G1_v1.root",
    "w" : "%s/w.root",
    "tt" : "%s/Muons_TTJets_TuneZ2_7TeV_madgraph_tauola_Spring11_PU_S1_START311_V1G1_v1.root",
    "z" : "%s/Muons_DYJetsToLL_TuneZ2_M_50_7TeV_madgraph_tauola_Spring11_PU_S1_START311_V1G1_v1.root",
    "lm1" : "%s/Muons_LM1_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
    "lm3" : "%s/Muons_LM3_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
    "lm6" : "%s/Muons_LM6_SUSY_sftsht_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root",
    "tanbeta10" : "%s/tanbeta10.root"
    }



# Name format of the histogram path
bin_fmt = "Counter_BSMGrid_%s%d%s/%s"
# Name of the counter histogram for SM MC
hname = "SM_Events"
# Which susyScan to use
susyScan = "tanbeta10"
# Paths to kfactor files for getting NLO xsections
kfactor_files = {
    "tanbeta10" : "/vols/cms03/as1604/ra4/hadronic/python/hadronic/scale_xsection_nlo1.0_tanssdat10.txt"
    }
# use NLO signal xs for limit?
use_nloxs = False

# Constants used in limit-setting
constants = {
    "lumi"        : 2000.0,       # Integrated luminosity to use for limit setting/systs
    "lumiError"   : 0.04,         # Relative error on luminosity estimate (for limit setting)
    "icf_default" : 100.0         # Default luminosity from ICF code
    }

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

includeSignalSysts = [
    "jec",
    ]
includeBackgroundSysts = [
    "jec",
    "metres",
    "Wtt"
    ]
