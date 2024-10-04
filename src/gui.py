import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QComboBox, QFileDialog, QMessageBox,
    QListWidget, QListWidgetItem, QProgressBar
)
from PyQt5.QtCore import Qt

# Importer les modules nécessaires
from twitch_api import TwitchAPI
from downloader import download_clip, sanitize_filename

class TwitchToTikTokGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.clips = []
        self.save_directory = ''
        # Initialiser l'API Twitch avec vos identifiants
        self.twitch_api = TwitchAPI(
            client_id=os.getenv('TWITCH_CLIENT_ID'),
            client_secret=os.getenv('TWITCH_CLIENT_SECRET')
        )

    def init_ui(self):
        self.setWindowTitle('Twitch to TikTok Downloader')
        self.setGeometry(100, 100, 400, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Label de bienvenue
        label = QLabel('Sélectionnez la période pour les meilleurs clips Twitch:')
        layout.addWidget(label)

        # ComboBox pour sélectionner la période
        self.combo_period = QComboBox()
        self.combo_period.addItems(['Jour', 'Semaine', 'Mois', 'Tous'])
        layout.addWidget(self.combo_period)

        # Bouton pour récupérer les clips
        self.btn_fetch = QPushButton('Récupérer les clips')
        self.btn_fetch.clicked.connect(self.fetch_clips)
        layout.addWidget(self.btn_fetch)

        # Liste des clips récupérés
        self.clips_list = QListWidget()
        layout.addWidget(self.clips_list)

        # Bouton pour sélectionner le dossier de sauvegarde
        self.btn_save = QPushButton('Sélectionner le dossier de sauvegarde')
        self.btn_save.clicked.connect(self.select_save_directory)
        layout.addWidget(self.btn_save)

        # Bouton pour télécharger les clips
        self.btn_download = QPushButton('Télécharger les clips')
        self.btn_download.clicked.connect(self.download_clips)
        self.btn_download.setEnabled(False)
        layout.addWidget(self.btn_download)

        # Barre de progression
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Définir le layout principal
        self.setLayout(layout)

    def fetch_clips(self):
        # Fonction pour récupérer les clips en fonction de la période sélectionnée
        period_mapping = {
            'Jour': 'day',
            'Semaine': 'week',
            'Mois': 'month',
            'Tous': 'all'
        }
        period = self.combo_period.currentText()
        period_value = period_mapping.get(period, 'day')
        print(f'Récupération des clips pour la période: {period_value}')

        try:
            # Récupérer les streamers en direct
            broadcaster_ids = self.twitch_api.get_live_streamers(language='fr', first=10)
            # Récupérer les clips pour ces streamers
            self.clips = self.twitch_api.get_top_clips(broadcaster_ids, period=period_value, first=10)
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f'Une erreur est survenue lors de la récupération des clips:\n{e}')
            return

        # Mise à jour de la liste des clips
        self.clips_list.clear()
        for clip in self.clips:
            item_text = f"{clip['title']} - {clip['broadcaster_name']} ({clip['view_count']} vues)"
            item = QListWidgetItem(item_text)
            item.setCheckState(Qt.Unchecked)
            self.clips_list.addItem(item)

        self.btn_download.setEnabled(True)

    def select_save_directory(self):
        # Fonction pour sélectionner le répertoire de sauvegarde
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(
            self,
            "Sélectionnez le dossier de sauvegarde",
            "",
            options=options
        )
        if directory:
            print(f'Dossier de sauvegarde sélectionné: {directory}')
            # Enregistrer le dossier sélectionné pour les téléchargements
            self.save_directory = directory

    def download_clips(self):
        # Vérifier si le dossier de sauvegarde a été sélectionné
        if not self.save_directory:
            QMessageBox.warning(self, 'Dossier non sélectionné', 'Veuillez sélectionner un dossier de sauvegarde.')
            return

        # Récupérer les clips sélectionnés
        selected_clips = []
        for index in range(self.clips_list.count()):
            item = self.clips_list.item(index)
            if item.checkState() == Qt.Checked:
                selected_clips.append(self.clips[index])

        if not selected_clips:
            QMessageBox.warning(self, 'Aucun clip sélectionné', 'Veuillez sélectionner au moins un clip à télécharger.')
            return

        print('Téléchargement des clips...')
        self.progress_bar.setMaximum(len(selected_clips))
        self.progress_bar.setValue(0)

        # Télécharger les clips sélectionnés
        for i, clip in enumerate(selected_clips, 1):
            try:
                filename = sanitize_filename(f"{clip['title']}.mp4")
                download_clip(clip['url'], self.save_directory, filename)
                self.progress_bar.setValue(i)
            except Exception as e:
                QMessageBox.critical(self, 'Erreur', f'Erreur lors du téléchargement de {clip["title"]}:\n{e}')

        QMessageBox.information(self, 'Téléchargement terminé', 'Les clips ont été téléchargés avec succès.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = TwitchToTikTokGUI()
    gui.show()
    sys.exit(app.exec_())