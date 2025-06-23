👇 Copie-colle ce bloc **tel quel** dans ton `README.md`.
(Il conserve les parties “locales” que tu avais déjà, et ajoute tout le nécessaire pour le déploiement : création du dossier `_credentials`, clé SSH, Terraform, Ansible, diagramme d’architecture, etc.)

```markdown
# 🧠 Projet MLOps – Pipeline d’entraînement & API (Docker / Terraform / Ansible / MLflow)

Ce dépôt propose deux manières de lancer le pipeline :

1. **Local** (Docker Compose) – idéal pour tester sur votre machine.  
2. **Cloud** (AWS EC2) – provisionné avec **Terraform**, configuré avec **Ansible**.

---

## 0. Prérequis rapides

| Outil | Version conseillée | Rôle |
|-------|-------------------|------|
| Docker & Docker Compose | ≥ 24 | Conteneurisation |
| Python | ≥ 3.10 | Scripts ML |
| Terraform | ≥ 1.6 | Provisionnement EC2 |
| Ansible | ≥ 2.15 | Configuration distante |
| Compte AWS + clé SSH | — | Exécution dans AWS |

---

## 1. Arborescence du projet

```

.
├── Dockerfile                # Image d’entraînement (prepare + train)
├── Dockerfile.api            # Image FastAPI
├── ansible/                  # Playbooks & inventaire
│   ├── inventory.ini         # À remplir avec les IP EC2
│   ├── playbook-api.yml      # Déploiement de l’API
│   └── playbook-training.yml # Entraînement modèle
├── api/                      # Code FastAPI
│   ├── main.py
│   └── wait\_for\_model.py
├── data/                     # Données + script de vérif
│   ├── housing\_raw\.csv
│   └── verify\_data.py
├── training/                 # Script d’entraînement
│   └── train.py
├── prepare\_data.py           # Nettoyage / features
├── requirements.txt          # Dépendances Python
├── tofu/                     # Code Terraform (EC2 + SG)
│   └── main.tf
├── docker-compose.yml        # Orchestration locale
├── orchestrate.sh / .bat     # Lancement local tout-en-un
└── \_credentials/             # 💡 À créer : clés AWS & SSH

````

---

## 2. Mise en place des **identifiants** (dossier `_credentials/`)

1. Crée le dossier `_credentials/` à la racine.  
2. **AWS** : ajoute le fichier `aws_learner_lab_credentials` (format standard `~/.aws/credentials`).  
3. **SSH** : place ta clé privée `labsuser.pem` dans ce même dossier **et** dans `~/.ssh/`.

```bash
chmod 400 ~/.ssh/labsuser.pem           # sécurité
````

> Le `main.tf` référence directement `_credentials/aws_learner_lab_credentials`.

---

## 3. Déploiement **Cloud** (Terraform ➜ Ansible)

### 3-1. Provisionner deux instances EC2

```bash
cd tofu
terraform init
terraform apply
```

> Terraform affiche deux sorties :
> `api_instance_public_ip` et `training_instance_public_ip`.

### 3-2. Compléter `ansible/inventory.ini`

```ini
[training]
ml-training ansible_host=<IP_TRAINING> ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/labsuser.pem

[api]
ml-api ansible_host=<IP_API> ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/labsuser.pem
```

➡️ **Remplace** `<IP_TRAINING>` et `<IP_API>` par les IP fournies par Terraform.

### 3-3. Lancer l’entraînement à distance

```bash
ansible-playbook -i ansible/inventory.ini ansible/playbook-training.yml
```

* Installe Docker sur `ml-training`
* Construit l’image `ml-train`
* Exécute `prepare_data.py` puis `train.py` (modèle sauvegardé dans `/home/ubuntu/ml_training/mlruns`).

### 3-4. Déployer l’API

```bash
ansible-playbook -i ansible/inventory.ini ansible/playbook-api.yml
```

* Installe Docker sur `ml-api`
* Copie le dernier modèle depuis `ml-training` (scp interne)
* Construit l’image `ml-api` et démarre FastAPI (port 8000).

### 3-5. Tester l’API à distance

```bash
# Interface Swagger
http://<IP_API>:8000/docs

# Exemple cURL
curl -X POST "http://<IP_API>:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"median_income":8.3,"housing_median_age":41,"rooms_per_household":7,
       "bedrooms_per_room":0.15,"population_per_household":2.5,
       "latitude":37.8,"longitude":-122.2}'
```

(Remplace `<IP_API>` par l’adresse de ton instance.)

---

## 4. Pipeline **local** (Docker Compose)

Pour un test rapide **sans AWS**.

### 4-1. Lancer le pipeline complet

* **Windows**

  ```bash
  .\orchestrate.bat
  ```

* **Linux / macOS**

  ```bash
  chmod +x orchestrate.sh
  ./orchestrate.sh
  ```

Une fois fini, rendez-vous sur [http://localhost:8000/docs](http://localhost:8000/docs).

### 4-2. Détails internes

1. **prepare\_data** → génère `data/housing_clean.csv`.
2. **train** → entraîne un modèle, log MLflow (`mlruns/`).
3. **api** → charge automatiquement le dernier modèle et expose `/predict`.

---

## 5. Diagramme d’architecture

```
                 ┌───────────────────────┐
                 │      Terraform        │
                 │  (VPC, 2× EC2, SG)    │
                 └──────────┬────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
┌──────────────────────┐        ┌──────────────────────┐
│  EC2 ① : ml-training │        │   EC2 ② : ml-api    │
│  - Docker            │        │  - Docker           │
│  - ml-train image    │        │  - ml-api image     │
│  - prepare_data.py   │  SCP   │  - FastAPI (8000)   │
│  - train.py + MLflow │ ─────► │  - wait_for_model   │
└──────────────────────┘        └──────────────────────┘
```

---

## 6. Nettoyer les ressources AWS

```bash
cd tofu
terraform destroy
```

---

### ✨ Remarques

* **Changement d’IP** : chaque `terraform apply` crée de nouvelles IP, pensez à mettre à jour `inventory.ini`.
* Les scripts d’orchestration locaux (`orchestrate.sh` / `.bat`) ne sont utiles que pour les tests **hors cloud**.

Bon déploiement ! 🚀
