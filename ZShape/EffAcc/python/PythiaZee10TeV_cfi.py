# this is a simple way of having a source which uses Pythia
# to produce Z events at LHC and force the decay to e+e-

import FWCore.ParameterSet.Config as cms

source = cms.Source("EmptySource")

generator = cms.EDFilter("Pythia6GeneratorFilter",

     # to printout pythia event record (call pylist)
     pythiaPylistVerbosity = cms.untracked.int32(0),

     # to printout HepMC::GenEvent record (HepMC::GenEvent::print())
     pythiaHepMCVerbosity = cms.untracked.bool(False),

     maxEventsToPrint = cms.untracked.int32(1),

     filterEfficiency = cms.untracked.double(1.000),
     comEnergy = cms.double(10000.0),
     crossSection = cms.untracked.double(1300),
     PythiaParameters = cms.PSet(

    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(1.000),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.untracked.double(10000.0),
    crossSection = cms.untracked.double(1944),
    maxEventsToPrint = cms.untracked.int32(0),

         parameterSets = cms.vstring(
             'pythiaUESettings', 
             'processParameters'
             ),

    pythiaUESettings = cms.vstring(
        'MSTJ(11)=3     ! Choice of the fragmentation function',
        'MSTJ(22)=2     ! Decay those unstable particles',
        'PARJ(71)=10 .  ! for which ctau  10 mm',
        'MSTP(2)=1      ! which order running alphaS',
        'MSTP(33)=0     ! no K factors in hard cross sections',
        'MSTP(51)=10042     ! CTEQ6L1 structure function chosen',
        'MSTP(52)=2     ! work with LHAPDF', 
        'MSTP(81)=1     ! multiple parton interactions 1 is Pythia default',
        'MSTP(82)=4     ! Defines the multi-parton model',
        'MSTU(21)=1     ! Check on possible errors during program execution',
        'PARP(82)=1.8387   ! pt cutoff for multiparton interactions',
        'PARP(89)=1960. ! sqrts for which PARP82 is set',
        'PARP(83)=0.5   ! Multiple interactions: matter distrbn parameter',
        'PARP(84)=0.4   ! Multiple interactions: matter distribution parameter',
        'PARP(90)=0.16  ! Multiple interactions: rescaling power',
        'PARP(67)=2.5    ! amount of initial-state radiation',
        'PARP(85)=1.0  ! gluon prod. mechanism in MI',
        'PARP(86)=1.0  ! gluon prod. mechanism in MI',
        'PARP(62)=1.25   ! ',
        'PARP(64)=0.2    ! ',
        'MSTP(91)=1     !',
        'PARP(91)=2.1   ! kt distribution',
        'PARP(93)=15.0  ! '
      ),

    processParameters = cms.vstring(
        "MSEL=0                  !User defined processes",
        "MSUB(1)=1               !Incl Z0/gamma* production",
        "MSTP(43)=3              !Both Z0 and gamma*", 
        "MDME(174,1)=0           !Z decay into d dbar",        
        "MDME(175,1)=0           !Z decay into u ubar",
        "MDME(176,1)=0           !Z decay into s sbar",
        "MDME(177,1)=0           !Z decay into c cbar",
        "MDME(178,1)=0           !Z decay into b bbar",
        "MDME(179,1)=0           !Z decay into t tbar",
        "MDME(182,1)=1           !Z decay into e- e+",
        "MDME(183,1)=0           !Z decay into nu_e nu_ebar",
        "MDME(184,1)=0           !Z decay into mu- mu+",
        "MDME(185,1)=0           !Z decay into nu_mu nu_mubar",
        "MDME(186,1)=0           !Z decay into tau- tau+",
        "MDME(187,1)=0           !Z decay into nu_tau nu_taubar",
        "CKIN(1)=40.       !Minimum sqrt(s_hat) value (=Z mass)"
    )

         

 )
)
