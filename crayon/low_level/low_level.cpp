#include <cpr/cpr.h>

#include <cstdlib>
#include <iostream>
#include <nlohmann/json.hpp>

class Ville {
  std::string _nom;
  int _code_postal;
  int _prix_m_2;

 public:
  Ville(std::string nom, int code_postal, int prix_m_2)
      : _nom{nom}, _code_postal{code_postal}, _prix_m_2{prix_m_2} {}
  friend std::ostream& operator<<(std::ostream& out, const Ville& ville) {
    return out << ville._nom << " : " << ville._code_postal << ", "
               << ville._prix_m_2 << " euros/m^2";
  }
  Ville(nlohmann::json j) {
    _nom = j["nom"];
    _code_postal = j["code_postal"];
    _prix_m_2 = j["prix_m_2"];
  }
  Ville(int id) {
    std::string url = "http://localhost:8000/ville/" + std::to_string(id);
    cpr::Response r = cpr::Get(cpr::Url{url});
    // r.status_code;
    nlohmann::json j = nlohmann::json::parse(r.text);
    _nom = j["nom"];
    _code_postal = j["code_postal"];
    _prix_m_2 = j["prix_m_2"];
  }

  auto get_nom() const -> std::string { return _nom; }
};

class Machine {
  std::string _nom;
  int _prix;
  int _n_serie;

 public:
  Machine(std::string nom, int prix, int n_serie)
      : _nom{nom}, _prix{prix}, _n_serie{n_serie} {}
  friend std::ostream& operator<<(std::ostream& out, const Machine& machine) {
    return out << machine._nom << " | numero : " << machine._n_serie
               << " | prix : " << machine._prix << " euros";
  }
  Machine(int id) {
    std::string url = "http://localhost:8000/machine/" + std::to_string(id);
    cpr::Response r = cpr::Get(cpr::Url{url});
    // r.status_code;
    nlohmann::json j = nlohmann::json::parse(r.text);
    _nom = j["nom"];
    _prix = j["prix"];
    _n_serie = j["n_serie"];
  }

  auto get_nom() const -> std::string { return _nom; }
};

class Usine {
  std::string _nom;
  std::unique_ptr<Ville> _ville;
  int _surface;
  std::vector<std::unique_ptr<Machine>> _machines;

 public:
  friend std::ostream& operator<<(std::ostream& out, const Usine& usine) {
    return out << usine._nom << " : " << usine._ville->get_nom() << ", "
               << usine._surface << " m^2";  //<< usine._machines.nom;
  }
  Usine(int id) {
    std::string url = "http://localhost:8000/usine/" + std::to_string(id);
    cpr::Response r = cpr::Get(cpr::Url{url});
    // r.status_code;
    nlohmann::json j = nlohmann::json::parse(r.text);
    _nom = j["nom"];
    _ville = std::make_unique<Ville>(j["ville"]);
    _surface = j["surface"];
    //_machines = j["machines"];
  }
};

auto main() -> int {
  std::cout << Ville(1) << std::endl;
  std::cout << Ville(3) << std::endl;
  std::cout << Machine(1) << std::endl;
  std::cout << Machine(2) << std::endl;
  std::cout << Usine(1) << std::endl;
  return 0;
}
