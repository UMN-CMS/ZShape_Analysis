// -*- C++ -*-
//
// Package:    McLevelEff
// Class:      ZEfficiencyCalculator
// 
/**\class ZEfficiencyCalculator ZEfficiencyCalculator.cc ZShape/EffAcc/src/ZEfficiencyCalculator.cc

Description: <one line class summary>

Implementation:
<Notes on implementation>
*/
//
// Original Author:  Giovanni FRANZONI
//         Created:  Thu Oct  4 11:30:13 CEST 2007
// $Id: ZEfficiencyCalculator.h,v 1.1 2007/10/26 23:02:09 franzoni Exp $
//
//


// system include files
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "SimDataFormats/HepMCProduct/interface/HepMCProduct.h"
#include "DataFormats/Common/interface/Handle.h"

#include <CLHEP/Vector/LorentzVector.h>

#include "ZShape/Base/interface/EtaAcceptance.h"
#include "ZShape/Base/interface/ZShapeEvent.h"
#include "ZShape/Base/interface/ZShapeZDef.h"
#include "ZShape/EffAcc/interface/EffHistos.h"
#include "ZShape/EffAcc/interface/EfficiencyStore.h"
#include "ZShape/EffAcc/interface/EfficiencyCut.h"


#include "TRandom3.h"
#include "TFile.h"


//
// class decleration
//

class ZEfficiencyCalculator : public edm::EDAnalyzer {
public:
  explicit ZEfficiencyCalculator(const edm::ParameterSet&);
  ~ZEfficiencyCalculator();


private:
  virtual void beginJob(const edm::EventSetup&) ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  
  void fillEvent(const HepMC::GenEvent* evt);
  void loadEfficiency(const std::string& name, const std::string& fname, const std::string& var);
  void acceptanceCuts();
  void applyEfficiencies();

  // ----------member data ---------------------------
  ZShapeEvent evt_;
  
  TRandom3 randomNum;

  std::string outFileName_;
  bool        writeHistoConservatively_;
  TFile*      histoFile_;

  // the efficiency objects
  std::map<std::string, EfficiencyStore*> efficiencies_;
  std::map<std::string, EfficiencyCut*> theCuts_;
  
  // object which applies the eta cuts
  EtaAcceptance theEtaSelector_;

  // Z Definitions
  std::map<std::string, ZShapeZDef*> zdefs_;

  // Z Plots
  EffHistos allCase_;
  struct ZPlots {
    ZPlots(int nc) : postCut_(nc) { }
    EffHistos acceptance_;
    std::vector<EffHistos> postCut_;
  };
  std::map<std::string,ZPlots*> zplots_;
};


/** TODO: 

    Efficiencies need to specify dependencies (eta, pT, etc) [current: hack]

    Randomization of efficiencies

 */
