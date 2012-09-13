// -*- C++ -*-
//
// Package:    MakeZEffTree
// Class:      MakeZEffTree
// 
/**\class MakeZEffTree MakeZEffTree.cc ZShape/MakeZEffTree/src/MakeZEffTree.cc

Description: [one line class summary]

Implementation:
[Notes on implementation]
*/
//
// Original Author:  Alexander Gude
//         Created:  Fri Sep 23 11:50:21 CDT 2011
// $Id: MakeZEffTree.cc,v 1.1 2011/11/10 18:04:25 gude Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "ZEffTree.h"

#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/EgammaReco/interface/SuperCluster.h"
#include "DataFormats/RecoCandidate/interface/RecoEcalCandidate.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

//
// class declaration
//

class MakeZEffTree : public edm::EDAnalyzer {
    public:
        explicit MakeZEffTree(const edm::ParameterSet&);
        ~MakeZEffTree();

        static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


    private:
        virtual void beginJob() ;
        virtual void analyze(const edm::Event&, const edm::EventSetup&);
        virtual void endJob() ;

        virtual void beginRun(edm::Run const&, edm::EventSetup const&);
        virtual void endRun(edm::Run const&, edm::EventSetup const&);
        virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
        virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

        bool ProbePassProbeOverlap(const reco::CandidateBaseRef& probe, edm::Handle<reco::CandidateView>& passprobes);
        bool MatchObjects(const reco::Candidate *hltObj, const reco::CandidateBaseRef& tagObj);
        // ----------member data ---------------------------
        ZEffTree *m_ze;
        edm::InputTag tnpProducer_;
        std::vector<edm::InputTag> passProbeCandTags_;
        double delRMatchingCut_, delPtRelMatchingCut_;
        std::vector<std::string> cutName_;

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
MakeZEffTree::MakeZEffTree(const edm::ParameterSet& iConfig) {
    //now do what ever initialization is needed
    edm::Service<TFileService> ts;
    TFile &f = ts->file();
    bool writable=true;
    m_ze = new ZEffTree(f,writable);

    tnpProducer_ = iConfig.getUntrackedParameter<edm::InputTag > ("TagProbeProducer");
    std::vector< edm::InputTag > defaultPassProbeCandTags;
    passProbeCandTags_ = iConfig.getUntrackedParameter< std::vector<edm::InputTag> >("passProbeCandTags", defaultPassProbeCandTags);

    delRMatchingCut_ = iConfig.getUntrackedParameter<double>("dRMatchCut", 0.2);
    delPtRelMatchingCut_ = iConfig.getUntrackedParameter<double>("dPtMatchCut", 15.0);
    cutName_ = iConfig.getUntrackedParameter< std::vector<std::string> >("CutNames");

}


MakeZEffTree::~MakeZEffTree() {
    // do anything here that needs to be done at desctruction time
    // (e.g. close files, deallocate resources etc.)
    //m_ze->Write();

}


//
// member functions
//

// ------------ method called for each event  ------------
void
MakeZEffTree::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    using namespace edm;

    m_ze->Clear();

    Handle<edm::HepMCProduct> HepMC;

    if (!iEvent.isRealData()) {
        iEvent.getByLabel("generator",HepMC);
        const HepMC::GenEvent* genE=HepMC->GetEvent();

        HepMC::GenEvent::vertex_const_iterator vtex;
        HepMC::GenVertex::particles_out_const_iterator Pout;
        HepMC::GenParticle* ge0=0;
        HepMC::GenParticle* ge1=0;
        HepMC::GenParticle* Z=0;
        for (vtex=genE->vertices_begin(); vtex!=genE->vertices_end(); vtex++){
            if (((*vtex)->particles_in_size())==1) {
                if ((*((*vtex)->particles_in_const_begin()))->pdg_id()==23){
                    Z=(*((*vtex)->particles_in_const_begin()));
                    for (Pout=(*vtex)->particles_out_const_begin(); Pout!=(*vtex)->particles_out_const_end(); Pout++){
                        if (abs((*Pout)->pdg_id())==11){
                            if(ge0==0){
                                ge0=*Pout;
                            } else {
                                ge1=*Pout;
                            }
                        }
                    }
                }
            } 
        }

        if (ge0==0 || ge1==0 || Z->momentum().m() < 40) {
            // Low mass or failed to get electrons
            return;
        }

        // ge0 is always the highest pt electron
        if (ge1->momentum().perp()>ge0->momentum().perp()) {
            std::swap(ge0,ge1);
        }

        edm::Handle<std::vector<PileupSummaryInfo> > pPU;
        iEvent.getByLabel("addPileupInfo", pPU);
        std::vector<PileupSummaryInfo>::const_iterator pPUI;

        int npv = 1; // Does not include primary vert
        for(pPUI = pPU->begin(); pPUI != pPU->end(); ++pPUI) {
            if (pPUI->getBunchCrossing() == 0) {
                npv = pPUI->getPU_NumInteractions() + 1;
                break;
            }
        }

        m_ze->gen.eta[0] = ge0->momentum().eta();
        m_ze->gen.eta[1] = ge1->momentum().eta();
        m_ze->gen.phi[0] = ge0->momentum().phi();
        m_ze->gen.phi[1] = ge1->momentum().phi();
        m_ze->gen.pt[0] = ge0->momentum().perp();
        m_ze->gen.pt[1] = ge1->momentum().perp();
        m_ze->gen.charge[0] = ge0->charge();
        m_ze->gen.charge[1] = ge1->charge();
        m_ze->gen.mz = Z->momentum().m();
        m_ze->gen.yz = 0.5*log((Z->momentum().e()+Z->momentum().pz())/(Z->momentum().e()-Z->momentum().pz()));
        m_ze->gen.qtz = Z->momentum().perp();
        m_ze->gen.nverts = npv;
    }

    edm::Handle<reco::CandidateView> tagprobes;
    if (!iEvent.getByLabel(tnpProducer_, tagprobes)) {
        LogWarning("ZFromData") << "Could not extract tag-probe map with input tag " << tnpProducer_;
        std::cout << "Didn't get the input tag " << std::endl;
    } else {
        if (tagprobes.isValid()) {
            //--Here I pick a random T&Probe combination based on the event number
            int tpsize = tagprobes->size();
            if (iEvent.isRealData() && tpsize == 0) {
                // No second electron
                return;
            }
            int usetp = (tpsize > 0) ? (iEvent.id().event()) % tpsize : 0;
            int tpnum = 0;
            //--End picking a random Tag and Probe combination
            //std::cout << " tpnum " << tpnum << " usetp " << usetp << " tpsize " << tpsize << std::endl;
            reco::CandidateView::const_iterator tpItr = tagprobes->begin();
            for (; tpItr != tagprobes->end(); ++tpItr, ++tpnum) {
                if (tpnum != usetp) continue;

                const reco::CandidateBaseRef &tag = tpItr->daughter(0)->masterClone();
                const reco::CandidateBaseRef &vprobes = tpItr->daughter(1)->masterClone();

                math::XYZTLorentzVector tpP4 = tag->p4() + vprobes->p4(); //Create Z p4 vector

                m_ze->reco.eta[0] = tag->p4().eta();
                m_ze->reco.eta[1] = vprobes->p4().eta();
                m_ze->reco.phi[0] = tag->p4().phi();
                m_ze->reco.phi[1] = vprobes->p4().phi(); 
                m_ze->reco.pt[0] = tag->p4().pt();
                m_ze->reco.pt[1] = vprobes->p4().pt();
                m_ze->reco.charge[0] = tag->charge();
                m_ze->reco.charge[1] = vprobes->charge();
                m_ze->reco.mz = tpP4.M();
                m_ze->reco.yz = tpP4.Rapidity();
                m_ze->reco.qtz = tpP4.pt();

                for (int itype = 0; itype < (int) passProbeCandTags_.size(); ++itype) {
                    //std::cout << "Looping over the types" << std::endl;
                    // Passing Probe Candidates
                    edm::Handle<reco::CandidateView> passprobes;
                    if (!iEvent.getByLabel(passProbeCandTags_[itype], passprobes)) {
                        LogWarning("ZFromData") << "Could not extract tag cands with input tag " << passProbeCandTags_[itype];
                        std::cout << "DIDn't get the darn tag..... " << std::endl;
                    }

                    ///int ppass = ProbePassProbeOverlap(vprobes[0].first,passprobes);
                    //std::cout << "doing the cuts themselves for " << passProbeCandTags_[itype] << std::endl;
                    m_ze->reco.setBit(0,cutName_[itype],ProbePassProbeOverlap(tag, passprobes));
                    m_ze->reco.setBit(1,cutName_[itype],ProbePassProbeOverlap(vprobes, passprobes));
                    //evt_.elec(0).cutResult(cutName_[itype], ProbePassProbeOverlap(tag, passprobes, exactMatch_[itype]));
                    //evt_.elec(1).cutResult(cutName_[itype], ProbePassProbeOverlap(vprobes, passprobes, exactMatch_[itype]));
                    //evt_.n_elec = 2;
                    // Did this tag cause a L1 and/or HLT trigger?
                    //bool l1Trigger = false;
                    //bool hltTrigger = false;
                }

            }


            /* Find the number of vertices */
            edm::Handle<reco::VertexCollection> recVtxs;
            iEvent.getByLabel("offlinePrimaryVertices",recVtxs);
            int nvert = 0;
            for(unsigned int ind=0;ind<recVtxs->size();ind++) {
                if (    
                        !((*recVtxs)[ind].isFake()) 
                        && ((*recVtxs)[ind].ndof()>4)
                        && (fabs((*recVtxs)[ind].z())<=24.0) 
                        && ((*recVtxs)[ind].position().Rho()<=2.0) 
                   ) {
                    nvert++;
                }
            }

            m_ze->reco.nverts = nvert;

        } else {
            std::cout << "Not Valid!!!!!!!!!!!!!" << std::endl;
        }
    }

    m_ze->Fill();
}

// ------------ method called once each job just before starting event loop  ------------
    void 
MakeZEffTree::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
    void 
MakeZEffTree::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
    void 
MakeZEffTree::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
    void 
MakeZEffTree::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
    void 
MakeZEffTree::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
    void 
MakeZEffTree::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MakeZEffTree::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
    //The following says we do not know what parameters are allowed so do no validation
    // Please change this to state exactly what you do use, even if it is no parameters
    edm::ParameterSetDescription desc;
    desc.setUnknown();
    descriptions.addDefault(desc);
}

bool MakeZEffTree::ProbePassProbeOverlap(const reco::CandidateBaseRef& probe, edm::Handle<reco::CandidateView>& passprobes) {
    bool ppass = 0;
    if (passprobes.isValid()) {
        for (int ipp = 0; ipp < (int) passprobes->size(); ++ipp) {
            bool isOverlap = MatchObjects(&((*passprobes)[ipp]), probe);
            if (isOverlap) {
                ppass = 1;
                continue;
            }

            reco::SuperClusterRef probeSC;
            reco::SuperClusterRef passprobeSC;

            if (not probe.isNull()) {
                probeSC = probe->get<reco::SuperClusterRef > ();
            }

            reco::CandidateBaseRef ref = passprobes->refAt(ipp);
            if (not ref.isNull()) {
                passprobeSC = ref->get<reco::SuperClusterRef > ();
            }

            isOverlap = isOverlap && (probeSC == passprobeSC);

            if (isOverlap) {
                ppass = 1;
            }
        }
    }
    return ppass;
}

bool MakeZEffTree::MatchObjects(const reco::Candidate *hltObj, const reco::CandidateBaseRef& tagObj) {
    double tEta = tagObj->eta();
    double tPhi = tagObj->phi();
    double tPt = tagObj->pt();
    double hEta = hltObj->eta();
    double hPhi = hltObj->phi();
    double hPt = hltObj->pt();

    double dRval = deltaR(tEta, tPhi, hEta, hPhi);
    double dPtRel = 999.0;
    if (tPt > 0.0) dPtRel = fabs(hPt - tPt) / tPt;

    // If we are comparing two objects for which the candidates should
    // be exactly the same, cut hard. Otherwise take cuts from user.
    //std::cout << " tEta " << tEta << " tPhi " << tPhi << " tPt " << tPt << " hEta " <<  hEta << " hPhi " << hPhi << " hPt " << hPt << std::endl;
    return ( dRval < delRMatchingCut_ && dPtRel < delPtRelMatchingCut_);
}


//define this as a plug-in
DEFINE_FWK_MODULE(MakeZEffTree);
