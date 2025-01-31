# Projet Django & C++ - Gestion des Villes et Usines

## 📌 Description
Ce projet réalisé dans un cadre académique combine **Django** (Python) pour la gestion de données et **C++** pour l’exploitation des données via une API.

- 🔹 **Django** : Création d’une API REST pour gérer des villes et des usines.
- 🔹 **C++** : Récupération des données via API et manipulation en local.

---

## 🚀 Installation

### 🛠 Prérequis
Assurez-vous d'avoir installé :
- **Git** :
- **Python** :
- **pip** :
- **venv** :
- **CMake** :

---

### 🐍 Installation du projet Django

1. **Cloner le projet**
   ```bash
   git clone https://github.com/Gagou-04/Crayon.git
   cd Crayon
   ```

2. **Créer un environnement virtuel et installer les dépendances**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # sous Linux
   pip install -r requirements.txt
   ```

3. **Configurer la base de données**
   ```bash
   ./manage.py makemigrations
   ./manage.py migrate
   ```

4. **Créer un superutilisateur (optionnel)**
   ```bash
   ./manage.py createsuperuser
   ```

5. **Lancer le serveur**
   ```bash
   ./manage.py runserver
   ```

---

### ⚙️ Compilation du projet C++

1. **Installer CMake**
   ```bash
   pip install cmake
   ```

2. **Cloner le projet et compiler**
   ```bash
   mkdir low_level
   cd low_level
   wget https://gitlab.laas.fr/gsaurel/teach/-/raw/main/src/CMakeLists.txt
   cmake -B build -S .
   cmake --build build
   ```

3. **Exécuter le programme**
   ```bash
   ./build/low_level
   ```

---

## 🔗 API Django

### **Endpoints principaux**
| Méthode | Endpoint | Description |
|---------|---------|------------|
| GET | `/api/villes/` | Liste des villes |
| GET | `/api/usines/` | Liste des usines |
| POST | `/api/usines/` | Ajouter une usine |
| GET | `/api/villes/{id}/` | Détails d'une ville |
| GET | `/api/usines/{id}/` | Détails d'une usine |

### **Exemple d’appel API**
```bash
curl -X GET http://localhost:8000/api/villes/ -H "Accept: application/json"
```

---

## 🧪 Tests

### **Django**
Lancer les tests unitaires :
```bash
./manage.py test
```

### **C++**
Exécuter et vérifier la récupération des données JSON.

---

## 🤝 Contribution
1. **Fork** le projet.
2. Crée une **branche** (`git checkout -b feature-nom`).
3. Fais un **commit** (`git commit -m "Ajout d'une fonctionnalité"`).
4. **Push** (`git push origin feature-nom`).
5. Crée une **Pull Request**.

---

## 📧 Contact
- **Nom** : CHAPPUT Gaetan & NGUYEN James
- **Email** : chapputgaetan@gmail.com & james.nguyen42@outlook.com
- **GitHub** : [Gagou-04](https://github.com:Gagou-04/Crayon.git)
