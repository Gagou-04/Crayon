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
               << ville._prix_m_2 << " m^2";
  }
  Ville(int id) {
    std::string url = "http://localhost:8000/ville/" + std::to_string(id);
    cpr::Response r = cpr::Get(cpr::Url{url});
    // r.status_code;
    // r.header["content-type"];
    // r.text;
    nlohmann::json j = nlohmann::json::parse(r.text);
    _nom = j["nom"];
    _code_postal = j["code_postal"];
    _prix_m_2 = j["prix_m_2"];
  }
};

auto main() -> int {
  std::cout << Ville(1) << std::endl;
  std::cout << Ville(3) << std::endl;
  return 0;
}
