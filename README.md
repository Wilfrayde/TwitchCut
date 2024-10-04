# TwitchCut

Ce programme vous permet de télécharger des clips Twitch et de les convertir au format TikTok. Il est conçu pour fonctionner sur un système Ubuntu et utilise PyQt5 pour l'interface graphique.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre système :

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

## Configuration

1. **Cloner le dépôt** : Téléchargez le code source du programme.
   ```bash
   git clone https://github.com/votre-utilisateur/TwitchCut.git
   cd TwitchCut
   ```

2. **Configurer les Identifiants Twitch** : Vous devez obtenir un `client_id` et un `client_secret` de l'API Twitch. Suivez ces étapes :
   - Créez une application sur le [Twitch Developer Portal](https://dev.twitch.tv/console/apps).
   - Notez votre `client_id` et `client_secret`.

3. **Définir les Variables d'Environnement** : Ajoutez vos identifiants Twitch à votre environnement. Vous pouvez le faire en ajoutant les lignes suivantes à votre fichier `~/.bashrc` :
   ```bash
   export TWITCH_CLIENT_ID='votre_client_id'
   export TWITCH_CLIENT_SECRET='votre_client_secret'
   ```
   Puis, rechargez votre fichier de configuration :
   ```bash
   source ~/.bashrc
   ```

## Exécution du Programme

1. **Activer l'Environnement Virtuel** : Si vous utilisez un environnement virtuel, activez-le :
   ```bash
   source env/bin/activate
   ```

2. **Lancer l'Application** : Exécutez le programme avec la commande suivante :
   ```bash
   python src/gui.py
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