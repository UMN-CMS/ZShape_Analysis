#ifndef ZShapeElectron_h_included
#define ZShapeElectron_h_included 1

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/Point3D.h"
#include <ostream>
#include <string>
#include <map>

class ZShapeElectron {
public:
  bool passed(const std::string& cutName) const; // false if not present!
  void cutResult(const std::string& cutName, bool didpass);
  void setWeight(const std::string& cutName, bool didpass);
  void setWeight(const std::string& cutName,double wgt);
  double weight(const std::string& cutName) const;
  // four-vector of electron (standardized, in physics space)
  math::PtEtaPhiMLorentzVector p4_;

  int charge_;
  int PU_;
  double detEta_;
  double detEtaVtx_;
  double scEnergy_;
  double detPhi_;
  double PS_;
  // calculate detector eta w.r.t to vertex
  double detectorEta(const math::XYZPoint& vtx) const;

  void dump(std::ostream& s) const;
  void clear();
private:
  // pass/fail for each possible cut
  std::map<std::string, bool> cutMap_;
  std::map<std::string, double> wgtMap_;
};


#endif // ZShapeElectron_h_included
