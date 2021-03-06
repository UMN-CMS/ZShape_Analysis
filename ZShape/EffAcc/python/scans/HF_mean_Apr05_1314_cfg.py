import FWCore.ParameterSet.Config as cms

process = cms.Process("Zefficiency")
process.TimerService = cms.Service("TimerService")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    SkipEvent = cms.untracked.vstring('ProductNotFound') 
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(40000)
    )

process.source = cms.Source("PoolSource",
                            duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring("file:/home/jmmans/data/zshape/Summer11_DYToEE_M-20_CT10_TuneZ2_7TeV-powheg-pythia/F61A0CD6-9AA8-E011-A92B-0024E8769B05.root" )
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('histo_10M_partBUILDINGTTEST.root')
)

process.f2s = cms.EDProducer("ZFullSim2Event"
                             )
import ZShape.EffAcc.FullSimSmearedElectronProducer_cfi
import ZShape.EffAcc.ZEfficiencyKevin_cfi


process.HFXmeanX0X90Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X90Xsmear.HF.meanp = cms.double(0.90)
process.HFXmeanX0X90Xsmear.HF.meanm = cms.double(0.90)

process.HFXmeanX0X90 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X90.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X90.zsrc = cms.untracked.InputTag("HFXmeanX0X90Xsmear","ZEventParticles")
process.HFXmeanX0X90.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X90Xsmear","ZEventParticles")

process.HFXmeanX0X93Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X93Xsmear.HF.meanp = cms.double(0.93)
process.HFXmeanX0X93Xsmear.HF.meanm = cms.double(0.93)

process.HFXmeanX0X93 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X93.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X93.zsrc = cms.untracked.InputTag("HFXmeanX0X93Xsmear","ZEventParticles")
process.HFXmeanX0X93.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X93Xsmear","ZEventParticles")

process.HFXmeanX0X94Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X94Xsmear.HF.meanp = cms.double(0.94)
process.HFXmeanX0X94Xsmear.HF.meanm = cms.double(0.94)

process.HFXmeanX0X94 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X94.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X94.zsrc = cms.untracked.InputTag("HFXmeanX0X94Xsmear","ZEventParticles")
process.HFXmeanX0X94.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X94Xsmear","ZEventParticles")

process.HFXmeanX0X95Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X95Xsmear.HF.meanp = cms.double(0.95)
process.HFXmeanX0X95Xsmear.HF.meanm = cms.double(0.95)

process.HFXmeanX0X95 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X95.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X95.zsrc = cms.untracked.InputTag("HFXmeanX0X95Xsmear","ZEventParticles")
process.HFXmeanX0X95.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X95Xsmear","ZEventParticles")

process.HFXmeanX0X96Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X96Xsmear.HF.meanp = cms.double(0.96)
process.HFXmeanX0X96Xsmear.HF.meanm = cms.double(0.96)

process.HFXmeanX0X96 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X96.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X96.zsrc = cms.untracked.InputTag("HFXmeanX0X96Xsmear","ZEventParticles")
process.HFXmeanX0X96.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X96Xsmear","ZEventParticles")

process.HFXmeanX0X97Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X97Xsmear.HF.meanp = cms.double(0.97)
process.HFXmeanX0X97Xsmear.HF.meanm = cms.double(0.97)

process.HFXmeanX0X97 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X97.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X97.zsrc = cms.untracked.InputTag("HFXmeanX0X97Xsmear","ZEventParticles")
process.HFXmeanX0X97.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X97Xsmear","ZEventParticles")

process.HFXmeanX0X98Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X98Xsmear.HF.meanp = cms.double(0.98)
process.HFXmeanX0X98Xsmear.HF.meanm = cms.double(0.98)

process.HFXmeanX0X98 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X98.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X98.zsrc = cms.untracked.InputTag("HFXmeanX0X98Xsmear","ZEventParticles")
process.HFXmeanX0X98.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X98Xsmear","ZEventParticles")

process.HFXmeanX0X99Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X99Xsmear.HF.meanp = cms.double(0.99)
process.HFXmeanX0X99Xsmear.HF.meanm = cms.double(0.99)

process.HFXmeanX0X99 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X99.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X99.zsrc = cms.untracked.InputTag("HFXmeanX0X99Xsmear","ZEventParticles")
process.HFXmeanX0X99.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X99Xsmear","ZEventParticles")

process.HFXmeanX1X00Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX1X00Xsmear.HF.meanp = cms.double(1.00)
process.HFXmeanX1X00Xsmear.HF.meanm = cms.double(1.00)

process.HFXmeanX1X00 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX1X00.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX1X00.zsrc = cms.untracked.InputTag("HFXmeanX1X00Xsmear","ZEventParticles")
process.HFXmeanX1X00.zElectronsCollection = cms.untracked.InputTag("HFXmeanX1X00Xsmear","ZEventParticles")

process.HFXmeanX1X05Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX1X05Xsmear.HF.meanp = cms.double(1.05)
process.HFXmeanX1X05Xsmear.HF.meanm = cms.double(1.05)

process.HFXmeanX1X05 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX1X05.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX1X05.zsrc = cms.untracked.InputTag("HFXmeanX1X05Xsmear","ZEventParticles")
process.HFXmeanX1X05.zElectronsCollection = cms.untracked.InputTag("HFXmeanX1X05Xsmear","ZEventParticles")

process.load("RecoEgamma.EgammaHFProducers.hfEMClusteringSequence_cff")

process.p = cms.Path(process.hfRecoEcalCandidate+process.f2s
+ process.HFXmeanX0X90Xsmear
+ process.HFXmeanX0X90
+ process.HFXmeanX0X93Xsmear
+ process.HFXmeanX0X93
+ process.HFXmeanX0X94Xsmear
+ process.HFXmeanX0X94
+ process.HFXmeanX0X95Xsmear
+ process.HFXmeanX0X95
+ process.HFXmeanX0X96Xsmear
+ process.HFXmeanX0X96
+ process.HFXmeanX0X97Xsmear
+ process.HFXmeanX0X97
+ process.HFXmeanX0X98Xsmear
+ process.HFXmeanX0X98
+ process.HFXmeanX0X99Xsmear
+ process.HFXmeanX0X99
+ process.HFXmeanX1X00Xsmear
+ process.HFXmeanX1X00
+ process.HFXmeanX1X05Xsmear
+ process.HFXmeanX1X05
)
