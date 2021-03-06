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


process.HFXmeanX0X095Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X095Xsmear.HF.mean = cms.double(0.095)

process.HFXmeanX0X095 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X095.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X095.zsrc = cms.untracked.InputTag("HFXmeanX0X095Xsmear","ZEventParticles")
process.HFXmeanX0X095.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X095Xsmear","ZEventParticles")

process.HFXmeanX0X0955Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X0955Xsmear.HF.mean = cms.double(0.0955)

process.HFXmeanX0X0955 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X0955.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X0955.zsrc = cms.untracked.InputTag("HFXmeanX0X0955Xsmear","ZEventParticles")
process.HFXmeanX0X0955.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X0955Xsmear","ZEventParticles")

process.HFXmeanX0X096Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X096Xsmear.HF.mean = cms.double(0.096)

process.HFXmeanX0X096 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X096.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X096.zsrc = cms.untracked.InputTag("HFXmeanX0X096Xsmear","ZEventParticles")
process.HFXmeanX0X096.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X096Xsmear","ZEventParticles")

process.HFXmeanX0X0965Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X0965Xsmear.HF.mean = cms.double(0.0965)

process.HFXmeanX0X0965 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X0965.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X0965.zsrc = cms.untracked.InputTag("HFXmeanX0X0965Xsmear","ZEventParticles")
process.HFXmeanX0X0965.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X0965Xsmear","ZEventParticles")

process.HFXmeanX0X97Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X97Xsmear.HF.mean = cms.double(0.97)

process.HFXmeanX0X97 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X97.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X97.zsrc = cms.untracked.InputTag("HFXmeanX0X97Xsmear","ZEventParticles")
process.HFXmeanX0X97.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X97Xsmear","ZEventParticles")

process.HFXmeanX0X975Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X975Xsmear.HF.mean = cms.double(0.975)

process.HFXmeanX0X975 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X975.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X975.zsrc = cms.untracked.InputTag("HFXmeanX0X975Xsmear","ZEventParticles")
process.HFXmeanX0X975.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X975Xsmear","ZEventParticles")

process.HFXmeanX0X98Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X98Xsmear.HF.mean = cms.double(0.98)

process.HFXmeanX0X98 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X98.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X98.zsrc = cms.untracked.InputTag("HFXmeanX0X98Xsmear","ZEventParticles")
process.HFXmeanX0X98.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X98Xsmear","ZEventParticles")

process.HFXmeanX0X985Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X985Xsmear.HF.mean = cms.double(0.985)

process.HFXmeanX0X985 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X985.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X985.zsrc = cms.untracked.InputTag("HFXmeanX0X985Xsmear","ZEventParticles")
process.HFXmeanX0X985.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X985Xsmear","ZEventParticles")

process.HFXmeanX0X99Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X99Xsmear.HF.mean = cms.double(0.99)

process.HFXmeanX0X99 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X99.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X99.zsrc = cms.untracked.InputTag("HFXmeanX0X99Xsmear","ZEventParticles")
process.HFXmeanX0X99.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X99Xsmear","ZEventParticles")

process.HFXmeanX0X995Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX0X995Xsmear.HF.mean = cms.double(0.995)

process.HFXmeanX0X995 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX0X995.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX0X995.zsrc = cms.untracked.InputTag("HFXmeanX0X995Xsmear","ZEventParticles")
process.HFXmeanX0X995.zElectronsCollection = cms.untracked.InputTag("HFXmeanX0X995Xsmear","ZEventParticles")

process.HFXmeanX1X0Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX1X0Xsmear.HF.mean = cms.double(1.0)

process.HFXmeanX1X0 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX1X0.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX1X0.zsrc = cms.untracked.InputTag("HFXmeanX1X0Xsmear","ZEventParticles")
process.HFXmeanX1X0.zElectronsCollection = cms.untracked.InputTag("HFXmeanX1X0Xsmear","ZEventParticles")

process.HFXmeanX1X005Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX1X005Xsmear.HF.mean = cms.double(1.005)

process.HFXmeanX1X005 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX1X005.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX1X005.zsrc = cms.untracked.InputTag("HFXmeanX1X005Xsmear","ZEventParticles")
process.HFXmeanX1X005.zElectronsCollection = cms.untracked.InputTag("HFXmeanX1X005Xsmear","ZEventParticles")

process.HFXmeanX1X01Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX1X01Xsmear.HF.mean = cms.double(1.01)

process.HFXmeanX1X01 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX1X01.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX1X01.zsrc = cms.untracked.InputTag("HFXmeanX1X01Xsmear","ZEventParticles")
process.HFXmeanX1X01.zElectronsCollection = cms.untracked.InputTag("HFXmeanX1X01Xsmear","ZEventParticles")

process.HFXmeanX1X015Xsmear = ZShape.EffAcc.FullSimSmearedElectronProducer_cfi.FullSimSmearedElectronsProducer.clone()
process.HFXmeanX1X015Xsmear.HF.mean = cms.double(1.015)

process.HFXmeanX1X015 = ZShape.EffAcc.ZEfficiencyKevin_cfi.mcEff.clone()
process.HFXmeanX1X015.zTreeLevelElectronsCollection = cms.untracked.InputTag("f2s","ZEventEle3")
process.HFXmeanX1X015.zsrc = cms.untracked.InputTag("HFXmeanX1X015Xsmear","ZEventParticles")
process.HFXmeanX1X015.zElectronsCollection = cms.untracked.InputTag("HFXmeanX1X015Xsmear","ZEventParticles")

process.load("RecoEgamma.EgammaHFProducers.hfEMClusteringSequence_cff")

process.p = cms.Path(process.hfRecoEcalCandidate+process.f2s
+ process.HFXmeanX0X095Xsmear
+ process.HFXmeanX0X095
+ process.HFXmeanX0X0955Xsmear
+ process.HFXmeanX0X0955
+ process.HFXmeanX0X096Xsmear
+ process.HFXmeanX0X096
+ process.HFXmeanX0X0965Xsmear
+ process.HFXmeanX0X0965
+ process.HFXmeanX0X97Xsmear
+ process.HFXmeanX0X97
+ process.HFXmeanX0X975Xsmear
+ process.HFXmeanX0X975
+ process.HFXmeanX0X98Xsmear
+ process.HFXmeanX0X98
+ process.HFXmeanX0X985Xsmear
+ process.HFXmeanX0X985
+ process.HFXmeanX0X99Xsmear
+ process.HFXmeanX0X99
+ process.HFXmeanX0X995Xsmear
+ process.HFXmeanX0X995
)
