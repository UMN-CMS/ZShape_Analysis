# produces cones around electrons type 1
# reconstructing electrons and provides smearing

import FWCore.ParameterSet.Config as cms

FullSimSmearedElectronsProducer = cms.EDProducer("ZSmearingProducer",
    zsrc = cms.untracked.InputTag("f2s","ZEventParticles"),
    zElectronsCollection = cms.untracked.InputTag("f2s","ZEventParticles"),
    doSmearing = cms.untracked.bool(True),
    doEB= cms.untracked.bool(True),
    doEE= cms.untracked.bool(True),
    doHFenergy= cms.untracked.bool(True),
    doHFeta= cms.untracked.bool(True),
    doHFphi= cms.untracked.bool(True),
    quiet = cms.untracked.bool(True),
    zElectronsCone = cms.double(0.08),
    randomSeed = cms.int32(134),
    SmearTable = cms.FileInPath('ZShape/EffAcc/data/CBBinsFile.txt'),
    HF = cms.PSet(
       stocastic = cms.double(0.0),
       constantp = cms.double(0.122),#uncert 0.02
       constantm = cms.double(0.0997),#uncert 0.0143
       constantp2 = cms.double(0.122),#uncert 0.02
       constantm2 = cms.double(0.0997),#uncert 0.0143
       fraction2 = cms.double(0.00),
       meanp = cms.double(0.965),  #uncert 0.007 
       meanm = cms.double(0.925),  #uncert 0.009
       reseta = cms.double(0.001),
       resphi = cms.double(0.001)
       ),
    EB = cms.PSet(
       p0 = cms.double(0.0) , 
       p1 = cms.double(0.0),
       p2 = cms.double(0.0),
       c = cms.double(0.0045),# uncertainty 0.0006 or 0.0061 with u 0.0008
       alpha = cms.double(1.0), #doesn't matter with n=0
       mean = cms.double(1.0028),  #uncertainty 0.00025
       n = cms.double(0.0)
   
    ),
     EE = cms.PSet(
   
        p0 = cms.double(0.0) , 
       p1 = cms.double(0.0),
       p2 = cms.double(0.0),
       c = cms.double(0.0155), #uncertainty 0.0017
       alpha = cms.double(1.0), #doesn't matter with n=0
       mean = cms.double(.990),  #uncertainty 0.0007
       n = cms.double(0.0)
   
    )
)
