import FWCore.ParameterSet.Config as cms

from PhysicsTools.HepMCCandAlgos.genParticles_cfi import *

#from PhysicsTools.TagAndProbe.tag_probe_electron_cfi import *

from RecoEgamma.EgammaHFProducers.hfEMClusteringSequence_cff import *

from Geometry.CMSCommonData.cmsIdealGeometryXML_cff import *

from Geometry.CaloEventSetup.CaloGeometry_cff import *

from Configuration.EventContent.EventContent_cff import *

#  electron isolation  ################
#
from RecoEgamma.EgammaIsolationAlgos.eleIsoFromDepsModules_cff import *
from RecoEgamma.EgammaIsolationAlgos.eleIsoDepositTk_cff import *
from RecoEgamma.EgammaIsolationAlgos.eleIsoDepositEcalFromHits_cff import *
from RecoEgamma.EgammaIsolationAlgos.eleIsoDepositHcalFromTowers_cff import *

hfEMClusters.correctionType = cms.int32(2)
hfRecoEcalCandidate.Correct = True
#hfRecoEcalCandidate.e9e25Cut = 0
hfRecoEcalCandidate.intercept2DCut = 0.32

hfSuperClusterCandidate = hfRecoEcalCandidate.clone()
hfSuperClusterCandidate.e9e25Cut = 0
hfSuperClusterCandidate.intercept2DCut = -99

hfRecoEcalCandidateTight = hfRecoEcalCandidate.clone()
hfRecoEcalCandidateTight.intercept2DCut = 0.45
#hfRecoEcalCandidateTight.e9e25Cut = 0


#  Calculate efficiency for *SuperClusters passing as GsfElectron* 
#
#  Tag           =  isolated GsfElectron with Robust ID, passing HLT, and  
#                    within the fiducial volume of ECAL
#  Probe --> Passing Probe   =  
#  SC --> GsfElectron --> isolation --> id --> Trigger
#############################################################

ELECTRON_ET_CUT_MIN = 20.0
HLTPath = "HLT_Ele17_SW_TightEleId_L1R"
RECO_NAME = "RECO"
#RECO_NAME = "reRECO"



##   ____                         ____ _           _            
##  / ___| _   _ _ __   ___ _ __ / ___| |_   _ ___| |_ ___ _ __ 
##  \___ \| | | | '_ \ / _ \ '__| |   | | | | / __| __/ _ \ '__|
##   ___) | |_| | |_) |  __/ |  | |___| | |_| \__ \ ||  __/ |   
##  |____/ \__,_| .__/ \___|_|   \____|_|\__,_|___/\__\___|_|   
##  
    ############################################# 
    ############  SuperClusters  ################
    ############################################# 

HybridSuperClusters = cms.EDProducer("ConcreteEcalCandidateProducer",
    src = cms.InputTag("correctedHybridSuperClusters","", RECO_NAME),
    particleType = cms.string('gamma')
)
EBSuperClusters = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("HybridSuperClusters"),
    cut = cms.string('abs( eta ) < 1.4442')
)

EndcapSuperClusters = cms.EDProducer("ConcreteEcalCandidateProducer",
    src = cms.InputTag("correctedMulti5x5SuperClustersWithPreshower","", RECO_NAME),
    particleType = cms.string('gamma')
)
EESuperClusters = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("EndcapSuperClusters"),
    cut = cms.string('abs( eta ) > 1.566 & abs( eta ) < 2.9')
)

allSuperClusters = cms.EDProducer("CandViewMerger",
    src = cms.VInputTag(cms.InputTag("EBSuperClusters"), cms.InputTag("EESuperClusters"),cms.InputTag("theHFSuperClusters"))
)




theHFSuperClusters = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("hfSuperClusterCandidate"),
    cut = cms.string('et > 15.0')
)


#superClusters = cms.EDFilter("SuperClusterMerger",
#   src = cms.VInputTag(cms.InputTag("correctedHybridSuperClusters","", RECO_NAME),
#                       cms.InputTag("correctedMulti5x5SuperClustersWithPreshower","", RECO_NAME)
 #                      #cms.InputTag("theHFSuperClusters","", RECO_NAME)
#                       ) 
#)

#superClusterCands = cms.EDProducer("ConcreteEcalCandidateProducer",
#   src = cms.InputTag("superClusters"),
#   particleType = cms.string('gamma'),
#)


# My final selection of superCluster candidates 
theSuperClusters = cms.EDFilter("CandViewSelector",
    #src = cms.InputTag("superClusterCands"),
    src = cms.InputTag("allSuperClusters"),
    cut = cms.string('et  > 20.0 && abs(eta)<2.9 && !(1.4442< abs(eta) <1.566)'),
    filter = cms.bool(True) #LOOK UP WHAT THIS DOES
)

NTElecLoose = cms.EDFilter("PhotonSelector",
                                   src = cms.InputTag("photons"),
                                   cut = cms.string("hadronicOverEm<0.07"
                                                    " && (superCluster.rawEnergy*sin(superCluster.position.theta)>20.0)"
                                                    " && (abs(superCluster.eta)>2.5) " # && abs(superCluster.eta)<2.8
                                                    " && (sigmaIetaIeta<0.03)"
                                                    " && (ecalRecHitSumEtConeDR03/(p4.Pt) < 0.06)"
                                                    " && (hcalTowerSumEtConeDR03/(p4.Pt) < 0.05)")
                                   )

NTElecTight = cms.EDFilter("PhotonSelector",
                                   src = cms.InputTag("photons"),
                                   cut = cms.string("hadronicOverEm<0.025"
                                                    " && (superCluster.rawEnergy*sin(superCluster.position.theta)>20.0)"
                                                    " && (abs(superCluster.eta)>2.5) " # && abs(superCluster.eta)<2.8
                                                    " && (sigmaIetaIeta<0.03)"
                                                    " && (ecalRecHitSumEtConeDR03/(p4.Pt) < 0.05)"
                                                    " && (hcalTowerSumEtConeDR03/(p4.Pt) < 0.025)")
                                   )



sc_sequence = cms.Sequence( ( hfSuperClusterCandidate * theHFSuperClusters + hfRecoEcalCandidateTight) * HybridSuperClusters * EBSuperClusters + EndcapSuperClusters * EESuperClusters * allSuperClusters * theSuperClusters +NTElecLoose + NTElecTight )



##
##     ___            ___    _ 
##    |_ _|___  ___  |_ _|__| | 
##     | |/ __|/ _ \  | |/ _` |
##     | |\__ \ (_)   | | (_| | 
##    |___|___/\___/ |___\__,_|
##


from ElectroWeakAnalysis.ZEE.simpleEleIdSequence_cff import *
from RecoEgamma.EgammaIsolationAlgos.egammaIsolationSequence_cff import *
from PhysicsTools.PatAlgos.patSequences_cff import *

patElectronIDs = cms.Sequence(simpleEleIdSequence)

#electronEcalRecHitIsolationLcone.ecalBarrelRecHitProducer = cms.InputTag("reducedEcalRecHitsEB")
#electronEcalRecHitIsolationScone.ecalBarrelRecHitProducer = cms.InputTag("reducedEcalRecHitsEB")
#electronEcalRecHitIsolationLcone.ecalEndcapRecHitProducer = cms.InputTag("reducedEcalRecHitsEE")
#electronEcalRecHitIsolationScone.ecalEndcapRecHitProducer = cms.InputTag("reducedEcalRecHitsEE")
#electronEcalRecHitIsolationLcone.ecalBarrelRecHitCollection = cms.InputTag("")
#electronEcalRecHitIsolationScone.ecalBarrelRecHitCollection = cms.InputTag("")
#electronEcalRecHitIsolationLcone.ecalEndcapRecHitCollection = cms.InputTag("")
#electronEcalRecHitIsolationScone.ecalEndcapRecHitCollection = cms.InputTag("")
patElectronIsolation = cms.Sequence(egammaIsolationSequence)


makePatElectrons = cms.Sequence(patElectronIDs*patElectronIsolation*patElectrons)

patElectrons.addElectronID = cms.bool(True)
patElectrons.electronIDSources = cms.PSet(
    simpleEleId95relIso= cms.InputTag("simpleEleId95relIso"),
    simpleEleId90relIso= cms.InputTag("simpleEleId90relIso"),
    simpleEleId85relIso= cms.InputTag("simpleEleId85relIso"),
    simpleEleId80relIso= cms.InputTag("simpleEleId80relIso"),
    simpleEleId70relIso= cms.InputTag("simpleEleId70relIso"),
    simpleEleId60relIso= cms.InputTag("simpleEleId60relIso"),
    simpleEleId95cIso= cms.InputTag("simpleEleId95cIso"),
    simpleEleId90cIso= cms.InputTag("simpleEleId90cIso"),
    simpleEleId85cIso= cms.InputTag("simpleEleId85cIso"),
    simpleEleId80cIso= cms.InputTag("simpleEleId80cIso"),
    simpleEleId70cIso= cms.InputTag("simpleEleId70cIso"),
    simpleEleId60cIso= cms.InputTag("simpleEleId60cIso"),
)
patElectrons.addGenMatch = cms.bool(False)
patElectrons.embedGenMatch = cms.bool(False)
patElectrons.isoDeposits = cms.PSet()
patElectrons.userIsolation = cms.PSet()

Iso95 =  cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') &&  (electronID("simpleEleId95relIso") > 6-0.1 && electronID("simpleEleId95relIso") < 7+.1)')                
)

ElectronID95 = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId95relIso") > 7-0.1 && electronID("simpleEleId95relIso") < 7+.1)')                
)

Iso90 =  cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && (electronID("simpleEleId90relIso") > 6-0.1 && electronID("simpleEleId90relIso") < 7+.1)')                

)

ElectronID90 = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId90relIso") == 7 )')
)

Iso85 =  cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId85relIso") == 6 || electronID("simpleEleId85relIso") == 7 )')                
)

ElectronID85 = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId85relIso") == 7 )')
)

Iso80 =  cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId80relIso") == 6 ||  electronID("simpleEleId80relIso") == 7 )')                
)

ElectronID80 = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId80relIso") == 7 )')
)

Iso70 =  cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId70relIso") == 6 || electronID("simpleEleId70relIso") == 7 )')                
)

ElectronID70 = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId70relIso") == 7 )')
)


Iso60 =  cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId60relIso") == 6 ||  electronID("simpleEleId60relIso") == 7 )')                
)

ElectronID60 = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId60relIso") == 7 )')
)

Iso80WConv = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId80relIso") == 6 ||  electronID("simpleEleId80relIso") == 7)')
)

Iso80Only = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId80relIso") == 2 ||  electronID("simpleEleId80relIso") == 3 || electronID("simpleEleId80relIso") == 6 ||  electronID("simpleEleId80relIso") == 7)')
)

ElectronID80Only  = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId80relIso") == 1 || electronID("simpleEleId80relIso") == 3 || electronID("simpleEleId80relIso") == 5 ||  electronID("simpleEleId80relIso") == 7 )')
)


ElectronID80WConv = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string('(ecalEnergy*sin(superClusterPosition.theta) >' + str(ELECTRON_ET_CUT_MIN) + ') && ( electronID("simpleEleId80relIso") == 5 ||  electronID("simpleEleId80relIso") == 7 )')
)




neweleseq=cms.Sequence(makePatElectrons* (Iso95 * ElectronID95 + Iso90 * ElectronID90 * Iso85 * ElectronID85 + Iso80 * ElectronID80+ Iso70 * ElectronID70 + Iso60 * ElectronID60 + Iso80Only + Iso80WConv + ElectronID80Only + ElectronID80WConv ) )




##    ____      __ _____ _           _                   
##   / ___|___ / _| ____| | ___  ___| |_ _ __ ___  _ __  
##  | |  _/ __| |_|  _| | |/ _ \/ __| __| '__/ _ \| '_ \ 
##  | |_| \__ \  _| |___| |  __/ (__| |_| | | (_) | | | |
##   \____|___/_| |_____|_|\___|\___|\__|_|  \___/|_| |_|
##  
    ############################################# 
    ############  GsfElectrons  ################
    #############################################
 
#theGsfElectrons = cms.EDFilter("GsfElectronRefSelector",
#    src = cms.InputTag("gsfElectrons"),
#    cut = cms.string('(abs(superCluster.eta)<2.5) && !(1.4442<abs(superCluster.eta)<1.566) && (( caloEnergy * sin( caloPosition.theta ) )  > 15.0)')
#)

PassingGsf = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("patElectrons"),
    cut = cms.string("(abs(superCluster.eta)<2.5) && !(1.4442<abs(superCluster.eta)<1.566)"
                     " && (ecalEnergy*sin(superClusterPosition.theta)>20.0) && (hadronicOverEm<0.15)")    
)

theGsfElectrons = PassingGsf.clone()

HFElectronID = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("hfRecoEcalCandidate"),
    cut = cms.string('et > 15.0')
)

HFElectronIDTight = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("hfRecoEcalCandidateTight"),
    cut = cms.string('et > 15.0')
)

theGsfHf = cms.EDProducer("CandViewMerger",
    #src = cms.VInputTag(cms.InputTag("theGsfElectrons"), cms.InputTag("theHFSuperClusters"), cms.InputTag("theEEHFGapSuperClusters"))
    src = cms.VInputTag(cms.InputTag("PassingGsf"), cms.InputTag("theHFSuperClusters"))
)


##     ___           _       _   _             
##    |_ _|___  ___ | | __ _| |_(_) ___  _ __  
##     | |/ __|/ _ \| |/ _` | __| |/ _ \| '_ \ 
##     | |\__ \ (_) | | (_| | |_| | (_) | | | |
##    |___|___/\___/|_|\__,_|\__|_|\___/|_| |_|

    
## #  Isolation  ################

theIsolation = Iso95.clone()

#theIsolation = cms.EDFilter("GsfElectronRefSelector",
#    src = cms.InputTag("gsfElectrons"),
#    cut = cms.string(PassingGsf.cut.value() +
#         " && (( isEB && (dr04TkSumPt<7.2) && (dr04EcalRecHitSumEt<5.7) && (dr04HcalTowerSumEt<8.1)"
#         " && (deltaEtaSuperClusterTrackAtVtx<0.0071) && (deltaPhiSuperClusterTrackAtVtx<1.0)"
#         " && (sigmaEtaEta<0.01))"
#         " || (isEE && (dr04TkSumPt<5.1) && (dr04EcalRecHitSumEt<5.0) && (dr04HcalTowerSumEt<3.4)"
#         " && (deltaEtaSuperClusterTrackAtVtx<0.0066) && (deltaPhiSuperClusterTrackAtVtx<1.0)"
#         " && (sigmaEtaEta<0.028)))")
#)

##    _____ _           _                     ___    _ 
##   | ____| | ___  ___| |_ _ __ ___  _ __   |_ _|__| |
##   |  _| | |/ _ \/ __| __| '__/ _ \| '_ \   | |/ _` |
##   | |___| |  __/ (__| |_| | | (_) | | | |  | | (_| |
##   |_____|_|\___|\___|\__|_|  \___/|_| |_| |___\__,_|
##   

# Electron ID  ######
#theId = cms.EDFilter("GsfElectronRefSelector",
#    src = cms.InputTag("gsfElectrons"),
#    cut = cms.string(theIsolation.cut.value() +
#          " && ( (isEB && sigmaIetaIeta<0.01 && deltaEtaSuperClusterTrackAtVtx<0.0071)"
#          "|| (isEE && sigmaIetaIeta<0.028 && deltaEtaSuperClusterTrackAtVtx<0.0066) )")   
#)
#

theId = ElectronID95.clone()

##    _____     _                         __  __       _       _     _             
##   |_   _| __(_) __ _  __ _  ___ _ __  |  \/  | __ _| |_ ___| |__ (_)_ __   __ _ 
##     | || '__| |/ _` |/ _` |/ _ \ '__| | |\/| |/ _` | __/ __| '_ \| | '_ \ / _` |
##     | || |  | | (_| | (_| |  __/ |    | |  | | (_| | || (__| | | | | | | | (_| |
##     |_||_|  |_|\__, |\__, |\___|_|    |_|  |_|\__,_|\__\___|_| |_|_|_| |_|\__, |
##                |___/ |___/                                                |___/ 
##   

# Trigger  ##################
theHLT = cms.EDProducer("trgMatchedGsfElectronProducer",                     
    InputProducer = cms.InputTag("theId"),                          
    hltTag = cms.untracked.VInputTag(
                cms.InputTag("HLT_Photon15_Cleaned_L1R","","HLT"),
                cms.InputTag("HLT_Ele15_SW_L1R","","HLT"),
                cms.InputTag("HLT_Ele15_SW_CaloEleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele17_SW_CaloEleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele17_SW_EleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele17_SW_TightEleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele17_SW_LooseEleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele27_SW_TightCaloEleIdTrack_L1R ","","HLT"),
                #cms.InputTag("HLT_Ele17_SW_TightCaloEleId_SC8HE_L1R","","HLT"),
                #cms.InputTag("HLT_Ele17_SW_TightCaloEleId_SC8HE_L1R_v1","","HLT"),
                #cms.InputTag("HLT_DoubleEle15_SW_L1R","","HLT"),
                #cms.InputTag("HLT_DoubleEle15_SW_L1R_v1","","HLT"),
                cms.InputTag("HLT_Ele22_SW_CaloEleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele17_SW_TighterEleIdIsol_L1R_v1","","HLT"),
                cms.InputTag("HLT_Ele17_SW_TighterEleIdIsol_L1R_v2","","HLT"),
                cms.InputTag("HLT_Ele17_SW_TighterEleIdIsol_L1R_v3","","HLT"),
                cms.InputTag("HLT_Ele22_SW_TighterEleId_L1R_v2","","HLT"),
                cms.InputTag("HLT_Ele22_SW_TighterCaloIdIsol_L1R_v1","","HLT"),
                #cms.InputTag("HLT_Ele17_SW_TightCaloEleId_Ele8HE_L1R","","HLT"),
                #cms.InputTag("HLT_Ele17_SW_TightCaloEleId_Ele8HE_L1R_v1","","HLT"),
                #cms.InputTag("HLT_DoubleEle17_SW_L1R","","HLT"),
                cms.InputTag("HLT_Ele32_SW_TighterEleId_L1R","","HLT")),
    triggerEventTag = cms.untracked.InputTag("hltTriggerSummaryAOD","","HLT")
)

theHLTGsf = cms.EDProducer("trgMatchedGsfElectronProducer",                     
    InputProducer = cms.InputTag("PassingGsf"),                          
    hltTag = cms.untracked.VInputTag(
                cms.InputTag("HLT_Photon15_Cleaned_L1R","","HLT"),
                cms.InputTag("HLT_Ele15_SW_L1R","","HLT"),
                cms.InputTag("HLT_Ele15_SW_CaloEleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele17_SW_CaloEleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele17_SW_EleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele17_SW_TightEleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele17_SW_LooseEleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele27_SW_TightCaloEleIdTrack_L1R ","","HLT"),
                #cms.InputTag("HLT_Ele17_SW_TightCaloEleId_SC8HE_L1R","","HLT"),
                #cms.InputTag("HLT_Ele17_SW_TightCaloEleId_SC8HE_L1R_v1","","HLT"),
                #cms.InputTag("HLT_DoubleEle15_SW_L1R","","HLT"),
                #cms.InputTag("HLT_DoubleEle15_SW_L1R_v1","","HLT"),
                cms.InputTag("HLT_Ele22_SW_CaloEleId_L1R","","HLT"),
                cms.InputTag("HLT_Ele17_SW_TighterEleIdIsol_L1R_v1","","HLT"),
                cms.InputTag("HLT_Ele17_SW_TighterEleIdIsol_L1R_v2","","HLT"),
                cms.InputTag("HLT_Ele17_SW_TighterEleIdIsol_L1R_v3","","HLT"),
                cms.InputTag("HLT_Ele22_SW_TighterEleId_L1R_v2","","HLT"),
                cms.InputTag("HLT_Ele22_SW_TighterCaloIdIsol_L1R_v1","","HLT"),
                #cms.InputTag("HLT_Ele17_SW_TightCaloEleId_Ele8HE_L1R","","HLT"),
                #cms.InputTag("HLT_Ele17_SW_TightCaloEleId_Ele8HE_L1R_v1","","HLT"),
                #cms.InputTag("HLT_DoubleEle17_SW_L1R","","HLT"),
                cms.InputTag("HLT_Ele32_SW_TighterEleId_L1R","","HLT")),                
    triggerEventTag = cms.untracked.InputTag("hltTriggerSummaryAOD","","HLT")
)

theGsfHFLoose =  cms.EDProducer("CandViewMerger",
    src = cms.VInputTag(cms.InputTag("PassingGsf"), cms.InputTag("HFElectronID"), cms.InputTag("NTElecLoose"))
)

electron_sequence = cms.Sequence(PassingGsf * theGsfElectrons * theHLTGsf * theGsfHf * theIsolation * theId * theHLT * (HFElectronID + HFElectronIDTight) * theGsfHFLoose )


##    _____ ___   ____    ____       _          
##   |_   _( _ ) |  _ \  |  _ \ __ _(_)_ __ ___ 
##     | | / _ \/\ |_) | | |_) / _` | | '__/ __|
##     | || (_>  <  __/  |  __/ (_| | | |  \__ \
##     |_| \___/\/_|     |_|   \__,_|_|_|  |___/
##                                              
##   
#  Tag & probe selection ######
    ################################################################ 
    ############  All Tag / Probe Association Maps  ###############
    ################################################################ 
    #// Remember that tag will always be "theHLT" collection.
    #//
    #// Probe can be one of the following collections: 
    #// "theSuperClusters", "theGsfElectrons", "theIsolation", "theId".
    #// 
    #// Passing Probe can be one of the following collections: 
    #// "theGsfElectrons", "theIsolation", "theId", "theHLT".
    #//




tpMapSuperClusters = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("theSuperClusters theSuperClusters"), # charge coniugate states are implied
    checkCharge = cms.bool(False),                           
    cut   = cms.string("30 < mass < 120"),
)


tpMapGsfElectrons = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("PassingGsf PassingGsf"), # charge coniugate states are implied
    cut   = cms.string("60 < mass < 120"),
    checkCharge = cms.bool(False),
)


tpMapIsolation = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("theHLT theIsolation"), # charge coniugate states are implied
    cut   = cms.string("60 < mass < 120"),
    checkCharge = cms.bool(False),
)

tpMapId =  cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("theHLT theId"), # charge coniugate states are implied
    cut   = cms.string("60 < mass < 120"),
    checkCharge = cms.bool(False),
)

tpMapHFSuperClusters = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("theHLT theHFSuperClusters"), # charge coniugate states are implied
    cut   = cms.string("30 < mass < 120"),
    checkCharge = cms.bool(False),
)



tpMapGsfAndHF =  cms.EDProducer("CandViewShallowCloneCombiner",
    #decay = cms.string("theHLTGsf theGsfHf"), # charge coniugate states are implied
    decay = cms.string("PassingGsf theGsfHf"),
    cut   = cms.string("50 < mass < 130"),
    checkCharge = cms.bool(False),
)

tpMapWP95AndHF =  cms.EDProducer("CandViewShallowCloneCombiner",
    #decay = cms.string("theHLTGsf theGsfHf"), # charge coniugate states are implied
    decay = cms.string("ElectronID95 theGsfHFLoose"),
    cut   = cms.string("50 < mass < 160"),
    checkCharge = cms.bool(False),
)




tpMap_sequence = cms.Sequence( tpMapSuperClusters + tpMapGsfElectrons + tpMapIsolation + tpMapId + tpMapHFSuperClusters + tpMapGsfAndHF + tpMapWP95AndHF)
#tpMap_sequence = cms.Sequence( tpMapGsfElectrons + tpMapIsolation + tpMapId + tpMapHFSuperClusters + tpMapGsfAndHF)

##    __  __  ____   __  __       _       _               
##   |  \/  |/ ___| |  \/  | __ _| |_ ___| |__   ___  ___ 
##   | |\/| | |     | |\/| |/ _` | __/ __| '_ \ / _ \/ __|
##   | |  | | |___  | |  | | (_| | || (__| | | |  __/\__ \
##   |_|  |_|\____| |_|  |_|\__,_|\__\___|_| |_|\___||___/
##                                                        


    ################################################################ 
    ############  All Truth-matched collections  ###################
    ################################################################ 
    #// find generator particles matching by DeltaR


SuperClustersMatch = cms.EDFilter("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(11),
    src = cms.InputTag("theSuperClusters"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles")
)

GsfElectronsMatch = cms.EDFilter("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(11),
    src = cms.InputTag("PassingGsf"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles")
)

IsolationMatch = cms.EDFilter("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(11),
    src = cms.InputTag("theIsolation"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles")
)

IdMatch = cms.EDFilter("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(11),
    src = cms.InputTag("theId"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles")
)

HLTMatch = cms.EDFilter("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(11),
    src = cms.InputTag("theHLT"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles")
)

HFSCMatch = cms.EDFilter("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(11),
    src = cms.InputTag("theHFSuperClusters"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles")
)

HFIDMatch = cms.EDFilter("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(11),
    src = cms.InputTag("HFElectronID"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles")
)


truthMatch_sequence = cms.Sequence( SuperClustersMatch + GsfElectronsMatch + IsolationMatch + IdMatch + HLTMatch + HFSCMatch + HFIDMatch)
#truthMatch_sequence = cms.Sequence( GsfElectronsMatch + IsolationMatch + IdMatch + HLTMatch + HFSCMatch + HFIDMatch)
#lepton_cands = cms.Sequence(genParticles * hfEMClusteringSequence * sc_sequence * electron_sequence * tpMap_sequence * truthMatch_sequence)

lepton_cands = cms.Sequence(hfEMClusteringSequence * sc_sequence * neweleseq * electron_sequence * tpMap_sequence )


   

