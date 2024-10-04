import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QProgressBar
)
from PyQt5.QtCore import Qt
from src.twitch_api import TwitchAPI
from src.downloader import download_clip, sanitize_filename  
from src.converter import ConversionThread, FetchClipsThread  

class TwitchToTikTokGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.clips = []
        self.threads = []
        self.save_directory = os.path.expanduser('~/Bureau/TwitchCut/clips')
        self.tiktok_directory = os.path.expanduser('~/Bureau/TwitchCut/clips_tiktok')
        os.makedirs(self.tiktok_directory, exist_ok=True)
        self.twitch_api = TwitchAPI(
            client_id=os.getenv('TWITCH_CLIENT_ID'),
            client_secret=os.getenv('TWITCH_CLIENT_SECRET')
        )

    def init_ui(self):
        self.setWindowTitle('Twitch to TikTok Downloader')
        self.setGeometry(100, 100, 400, 600)
        layout = QVBoxLayout()
        label = QLabel('Sélectionnez la période pour les meilleurs clips Twitch:')
        layout.addWidget(label)
        self.combo_period = QComboBox()
        self.combo_period.addItems(['Jour', 'Semaine', 'Mois', 'Tous'])
        layout.addWidget(self.combo_period)
        self.btn_fetch = QPushButton('Récupérer les clips')
        self.btn_fetch.clicked.connect(self.fetch_clips)
        layout.addWidget(self.btn_fetch)
        self.clips_list = QListWidget()
        layout.addWidget(self.clips_list)
        self.btn_save = QPushButton('Sélectionner le dossier de sauvegarde')
        self.btn_save.clicked.connect(self.select_save_directory)
        layout.addWidget(self.btn_save)
        self.btn_download = QPushButton('Télécharger les clips')
        self.btn_download.clicked.connect(self.download_clips)
        self.btn_download.setEnabled(False)
        layout.addWidget(self.btn_download)
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        self.status_label = QLabel('')
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def fetch_clips(self):
        period_mapping = {'Jour': 'day', 'Semaine': 'week', 'Mois': 'month', 'Tous': 'all'}
        period = self.combo_period.currentText()
        period_value = period_mapping.get(period, 'day')
        self.status_label.setText(f'Récupération des clips pour la période: {period_value}')
        self.btn_fetch.setEnabled(False)
        self.btn_download.setEnabled(False)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setValue(0)
        self.fetch_thread = FetchClipsThread(self.twitch_api, period_value)
        self.fetch_thread.clips_fetched.connect(self.on_clips_fetched)
        self.fetch_thread.error_occurred.connect(self.on_fetch_error)
        self.fetch_thread.start()

    def on_clips_fetched(self, clips):
        self.clips = clips
        self.progress_bar.setMaximum(1)
        self.progress_bar.setValue(1)
        self.btn_fetch.setEnabled(True)
        self.btn_download.setEnabled(True)
        self.status_label.setText('Clips récupérés avec succès.')
        self.clips_list.clear()
        for clip in self.clips:
            item_text = f"{clip['title']} - {clip['broadcaster_name']} ({clip['view_count']} vues)"
            item = QListWidgetItem(item_text)
            item.setCheckState(Qt.Unchecked)
            self.clips_list.addItem(item)

    def on_fetch_error(self, error_message):
        self.progress_bar.setMaximum(1)
        self.progress_bar.setValue(1)
        self.btn_fetch.setEnabled(True)
        QMessageBox.critical(self, 'Erreur', f'Une erreur est survenue lors de la récupération des clips:\n{error_message}')
        self.status_label.setText('Erreur lors de la récupération des clips.')

    def select_save_directory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Sélectionnez le dossier de sauvegarde", "", options=options)
        if directory:
            self.save_directory = directory
            self.status_label.setText(f'Dossier de sauvegarde sélectionné: {directory}')

    def download_clips(self):
        if not self.save_directory:
            QMessageBox.warning(self, 'Dossier non sélectionné', 'Veuillez sélectionner un dossier de sauvegarde.')
            return
        selected_clips = []
        for index in range(self.clips_list.count()):
            item = self.clips_list.item(index)
            if item.checkState() == Qt.Checked:
                selected_clips.append(self.clips[index])
        if not selected_clips:
            QMessageBox.warning(self, 'Aucun clip sélectionné', 'Veuillez sélectionner au moins un clip à télécharger.')
            return
        self.status_label.setText('Téléchargement des clips en cours...')
        self.progress_bar.setMaximum(len(selected_clips))
        self.progress_bar.setValue(0)
        for i, clip in enumerate(selected_clips, 1):
            try:
                filename = sanitize_filename(f"{clip['title']}.mp4")
                download_clip(clip['url'], self.save_directory, filename)
                self.progress_bar.setValue(i)
            except Exception as e:
                QMessageBox.critical(self, 'Erreur', f'Erreur lors du téléchargement de {clip["title"]}:\n{e}')
        QMessageBox.information(self, 'Téléchargement terminé', 'Les clips ont été téléchargés avec succès.')
        self.status_label.setText('Téléchargement terminé.')
        self.process_clips()

    def process_clips(self):
        self.status_label.setText('Conversion des clips en cours...')
        self.progress_bar.setMaximum(len(os.listdir(self.save_directory)))
        self.progress_bar.setValue(0)
        for i, clip in enumerate(os.listdir(self.save_directory), 1):
            input_file = os.path.join(self.save_directory, clip)
            output_file = os.path.join(self.tiktok_directory, f'tiktok_{clip}')
            self.convert_to_tiktok_format(input_file, output_file, i)

    def convert_to_tiktok_format(self, input_file, output_file, index):
        thread = ConversionThread(input_file, output_file, index)
        thread.progress.connect(self.update_progress)
        thread.finished.connect(self.check_conversion_completion)
        self.threads.append(thread)
        thread.start()

    def update_progress(self, index):
        self.progress_bar.setValue(index)

    def check_conversion_completion(self):
        if all(not thread.isRunning() for thread in self.threads):
            self.status_label.setText('Conversion terminée.')
            QMessageBox.information(self, 'Conversion terminée', 'Tous les clips ont été convertis avec succès.')