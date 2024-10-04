import os
import subprocess
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_clip(clip_url, save_directory, filename):
    """
    Télécharge un clip depuis l'URL spécifiée en utilisant streamlink et l'enregistre dans le répertoire donné.

    :param clip_url: URL du clip à télécharger
    :param save_directory: Répertoire où enregistrer le clip
    :param filename: Nom du fichier pour le clip téléchargé
    """
    try:
        # Créer le répertoire de sauvegarde s'il n'existe pas
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        file_path = os.path.join(save_directory, filename)
        logger.info(f"Téléchargement du clip depuis {clip_url} vers {file_path}")

        # Utiliser streamlink pour télécharger la vidéo
        command = ['streamlink', clip_url, 'best', '-o', file_path]
        subprocess.run(command, check=True)

        logger.info(f"Clip téléchargé avec succès : {file_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erreur lors du téléchargement du clip avec streamlink : {e}")
        raise

def sanitize_filename(filename):
    """
    Nettoie le nom de fichier pour éviter les caractères non valides.

    :param filename: Nom de fichier à nettoyer
    :return: Nom de fichier nettoyé
    """
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()