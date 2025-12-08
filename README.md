# photosHub
Projet hub photos 

# Install photohub

# Guide de démarrage rapide : PhotoHub avec Docker

Ce guide va droit au but pour lancer le projet **PhotoHub** avec **Docker**.

---

### 1. Prérequis

- Git installé
- Docker Desktop installé et en cours d'exécution

---

### 2. Première installation (à faire une seule fois)

Cette procédure initialise l'environnement, y compris la base de données.

### Étape 1 : Cloner le projet

Ouvre un terminal, place-toi dans le dossier où tu veux stocker le projet, puis exécute :

```bash
git clone <URL_DU_DEPOT_GIT>
cd photosHub
```

### Étape 2 : Lancer l'environnement

Notre application a besoin que sa base de données soit prête avant de se lancer. Suis ces étapes dans l'ordre.

1. **Démarrer la base de données en arrière-plan :**
    
    ```bash
    docker-compose up -d db
    ```
    
2. **Initialiser la base de données :**
    
    Cette commande construit l'image de l'application (avec les dépendances de `requirements.txt`) et exécute le script de création des tables.
    
    ```bash
    docker-compose run --build --rm web flask create-db
    ```
    
    Tu dois voir le message :
    
    > Base de données initialisée.
    > 
3. **Lancer l'application :**
    
    Maintenant que tout est prêt, on lance tous les services.
    
    ```bash
    docker-compose up
    ```
    

L'application est maintenant accessible sur http://localhost:5001.

---

### 3. Workflow quotidien

Pour travailler sur le projet les jours suivants, les commandes sont plus simples.

- **Pour démarrer l'application :**
    
    ```bash
    docker-compose up
    ```
    
- **Pour arrêter l'application :**
    1. Fais `Ctrl + C` dans le terminal où l'application tourne.
    2. Puis, pour un arrêt propre :
        
        ```bash
        docker-compose down
        ```
        

---

### 4. Commandes utiles

### Mettre à jour les dépendances

Si le fichier `requirements.txt` a été modifié (par toi ou via un `git pull`), tu dois reconstruire l'image de l'application. Utilise `--build` au prochain lancement :

```bash
docker-compose up --build
```

### Réinitialiser la base de données

Si tu veux repartir de zéro (vider complètement la base de données), exécute cette commande.

> ⚠️ Attention : cette opération est **irréversible**.
> 
1. Arrête les conteneurs **et** supprime le volume de données de la BDD :
    
    ```bash
    docker-compose down -v
    ```
    
2. Après cela, tu devras refaire toute la procédure de **Première installation** (section 2).