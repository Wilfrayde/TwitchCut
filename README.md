# TwitchCut

Ce projet vous permet de télécharger des clips Twitch et de les convertir au format TikTok. Bien que l'upload automatique sur TikTok ne soit pas pris en charge, vous pouvez facilement gérer les clips téléchargés et convertis.

## Prérequis

### Pour Linux

1. **Python 3.8+** : Assurez-vous que Python est installé. Vous pouvez vérifier cela en exécutant `python3 --version` dans votre terminal.

2. **pip** : L'outil de gestion de paquets Python. Vérifiez son installation avec `pip --version`.

3. **FFmpeg** : Un outil pour manipuler des fichiers multimédias. Installez-le avec la commande suivante :
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

4. **PyQt5** : Pour l'interface graphique. Installez-le avec :
   ```bash
   pip install PyQt5
   ```

5. **Autres dépendances Python** : Installez les autres dépendances nécessaires avec le fichier `requirements.txt` :
   ```bash
   pip install -r requirements.txt
   ```

### Pour Windows

1. **Python 3.8+** : Téléchargez et installez Python depuis [python.org](https://www.python.org/downloads/). Assurez-vous de cocher l'option "Add Python to PATH" lors de l'installation.

2. **pip** : Est généralement inclus avec Python. Vérifiez son installation avec `pip --version` dans l'invite de commande.

3. **FFmpeg** : Téléchargez FFmpeg depuis [ffmpeg.org](https://ffmpeg.org/download.html). Extrayez les fichiers et ajoutez le chemin du dossier `bin` de FFmpeg à votre variable d'environnement PATH.

4. **PyQt5** : Installez-le avec :
   ```cmd
   pip install PyQt5
   ```

5. **Autres dépendances Python** : Installez les autres dépendances nécessaires avec le fichier `requirements.txt` :
   ```cmd
   pip install -r requirements.txt
   ```

## Configuration

1. **Cloner le dépôt** : Téléchargez le code source du programme.
   ```bash
   git clone https://github.com/Wilfrayde/TwitchCut.git
   cd TwitchCut
   ```

2. **Configurer les Identifiants Twitch** : Vous devez obtenir un `client_id` et un `client_secret` de l'API Twitch. Suivez ces étapes :
   - Créez une application sur le [Twitch Developer Portal](https://dev.twitch.tv/console/apps).
   - Notez votre `client_id` et `client_secret`.

3. **Définir les Variables d'Environnement** :

   - **Pour Linux** : Ajoutez vos identifiants Twitch à votre environnement en modifiant `~/.bashrc` :
     ```bash
     export TWITCH_CLIENT_ID='votre_client_id'
     export TWITCH_CLIENT_SECRET='votre_client_secret'
     source ~/.bashrc
     ```

   - **Pour Windows** : Ajoutez vos identifiants Twitch aux variables d'environnement via le Panneau de configuration > Système > Paramètres système avancés > Variables d'environnement.

## Exécution du Programme

1. **Activer l'Environnement Virtuel** (optionnel mais recommandé) :

   - **Pour Linux** :
     ```bash
     source env/bin/activate
     ```

   - **Pour Windows** :
     ```cmd
     .\env\Scripts\activate
     ```

2. **Lancer l'Application** : Exécutez le programme avec la commande suivante depuis la racine du projet :

   - **Pour Linux** :
     ```bash
     python main.py
     ```

   - **Pour Windows** :
     ```cmd
     python main.py
     ```

## Utilisation

1. **Sélectionner la Période** : Choisissez la période pour laquelle vous souhaitez récupérer les clips Twitch (Jour, Semaine, Mois, Tous).

2. **Récupérer les Clips** : Cliquez sur "Récupérer les clips" pour obtenir les clips populaires de la période sélectionnée.

3. **Sélectionner le Dossier de Sauvegarde** : Choisissez où vous souhaitez enregistrer les clips téléchargés.

4. **Télécharger les Clips** : Sélectionnez les clips que vous souhaitez télécharger et cliquez sur "Télécharger les clips".

5. **Conversion au Format TikTok** : Les clips téléchargés seront automatiquement convertis au format TikTok.

## Dépannage

- **Problèmes de Permission** : Assurez-vous que vous avez les permissions nécessaires pour écrire dans le répertoire de sauvegarde.
- **Erreurs de Conversion** : Vérifiez que FFmpeg est correctement installé et accessible depuis votre terminal.
- **Problèmes de Connexion** : Assurez-vous que votre connexion Internet est active et que vos identifiants Twitch sont corrects.

## Contributions

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.