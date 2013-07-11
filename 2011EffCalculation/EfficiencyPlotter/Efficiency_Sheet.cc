#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <iostream>
#include <map>

#ifndef Efficiency_Sheet
#define Efficiency_Sheet

class EffSheet{
    public:
        struct EffMapKey{
            double etamin;
            double etamax;
            double pumin;
            double pumax;
            bool phistar;

            bool operator()(const EffSheet::EffMapKey one, const EffSheet::EffMapKey other){
                // Pt < Phistar
                if (one.phistar && !other.phistar) {
                    return false;
                } else if (!one.phistar && other.phistar) {
                    return true;
                }

                // Eta Min
                if (one.etamin < other.etamin){
                    return true;
                } else if (one.etamin > other.etamin){
                    return false;
                }

                // Eta Max
                if (one.etamax < other.etamax){
                    return true;
                } else if (one.etamax > other.etamax){
                    return false;
                }

                //PU Min
                if (one.pumin < other.pumin){
                    return true;
                } else if (one.pumin > other.pumin){
                    return false;
                }

                //PU Max
                if (one.pumax < other.pumax){
                    return true;
                } else if (one.pumax > other.pumax){
                    return false;
                }

                // They are equal
                return false; 
            }
        };

        EffSheet(const std::string textFile);
        struct EffLine;
        struct EffMapKey;
        EffLine* current;
        std::map<EffMapKey, std::vector<EffLine>, EffMapKey > values;

    private:
};


struct EffSheet::EffLine{
    double xmin;
    double xmax;
    double etamin;
    double etamax;
    double pumin;
    double pumax;
    int numparms;
    double eff;
    double systp;
    double systm;
    double den;
    bool phistar;
};

EffSheet::EffSheet(const std::string textFile){
    /* Open file */
    std::ifstream inFile(textFile.c_str());
    std::string line;

    /* Loop through lines */
    while( std::getline(inFile, line) ){
        if (line[0] != '#'){ // Skip comments
            std::string item;
            std::vector<std::string> items;
            std::stringstream ss(line);

            EffSheet::EffLine value;
            ss >> value.xmin;
            ss >> value.xmax;
            ss >> value.etamin;
            ss >> value.etamax;
            ss >> value.pumin;
            ss >> value.pumax;
            ss >> value.numparms;
            ss >> value.eff;
            ss >> value.systp;
            ss >> value.systm;
            ss >> value.den;
            ss >> value.phistar;

            /* Place in container via map */
            EffSheet::EffMapKey emk;
            emk.etamin = value.etamin;
            emk.etamax = value.etamax;
            emk.pumin = value.pumin;
            emk.pumax = value.pumax;
            emk.phistar = value.phistar;

            /* If we don't already have this value */
            //if (values.find(emk) == values.end()){
            //    std::vector<EffSheet::EffLine> tmpv;
            //    values[emk] = tmpv;
            //}

            values[emk].push_back(value);
        }
    }

    /* Close file */
    inFile.close();
}
#endif

/* Compile time notes:
 *    g++ -O2 -o Efficiency_Sheet.exe Efficiency_Sheet.cc `root-config --cflags --libs` 
 */
