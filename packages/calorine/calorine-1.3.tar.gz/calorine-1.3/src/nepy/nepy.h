#include "nep.h"

// Local struct to hold an atomic configuration.
struct Atom
{
    int N;
    std::vector<int> type;
    std::vector<double> cell, position;
};

class NEPY
{
private:
    NEP3 nep;
    struct Atom atom;
    std::string potential_filename;

public:
    NEPY(const std::string &potential_filename, int N_atoms, std::vector<double> box, std::vector<std::string> atom_symbols, std::vector<double> positions);
    std::vector<double> getDescriptors();
    std::tuple<std::vector<double>, std::vector<double>, std::vector<double>> getPotentialForcesAndVirials();
    std::vector<std::string> _getAtomSymbols(std::string potential_filename);
    void _convertAtomTypeNEPIndex(int N, std::vector<std::string> atom_symbols, std::vector<std::string> model_atom_symbols, std::vector<int> &type);
    void setPositions(std::vector<double> positions);
    void setCell(std::vector<double> cell);
    void setSymbols(std::vector<std::string> atom_symbols);
};