import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

source = cms.Source("EmptySource")


generator = cms.EDFilter("Pythia8ConcurrentGeneratorFilter",
   pythiaPylistVerbosity = cms.untracked.int32(0),
   filterEfficiency = cms.untracked.double(1.0),
   pythiaHepMCVerbosity = cms.untracked.bool(False),
   comEnergy = cms.double(13000.0),
   crossSection = cms.untracked.double(-1.0),
   maxEventsToPrint = cms.untracked.int32(0),
   crossSectionNLO = cms.untracked.double(-1.0),
   PythiaParameters = cms.PSet(
       pythia8CommonSettingsBlock,
       pythia8CP5SettingsBlock,
       pythia8PSweightsSettingsBlock,
       processParameters = cms.vstring('Main:timesAllowErrors    = 10000', 
           'ParticleDecays:limitTau0 = on', 
           'ParticleDecays:tau0Max   = 10.', 
           'Beams:allowVertexSpread = on', 
           'PhaseSpace:pTHatMin      = 0.', 
           'WeakSingleBoson:all = off', 
           'WeakSingleBoson:ffbar2W = on', 
           '24:onMode = off',
           '24:onIfAny = 11 -12',
           '24:onIfAny = 13 -14',
           '24:onIfAny = 15 -16',
           'WeakBosonAndParton:qqbar2Wg = on', 
           'WeakBosonAndParton:qg2Wq = on', 
           'SecondHard:generate = on', 
           'SecondHard:SingleW = on', 
           'SecondHard:WAndJet = on'),
       parameterSets = cms.vstring('pythia8CommonSettings',
                                   'pythia8CP5Settings',
                                   'pythia8PSweightsSettings',
                                   'processParameters')
   )
)
ProductionFilterSequence = cms.Sequence(generator)