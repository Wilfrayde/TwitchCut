import subprocess
from PyQt5.QtCore import QThread, pyqtSignal

class ConversionThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, input_file, output_file, index):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.index = index

    def run(self):
        command = [
            'ffmpeg',
            '-i', self.input_file,
            '-vf', 'scale=1080:-1,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-f', 'mp4',
            self.output_file
        ]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f'Error converting {self.input_file}: {e}')
        self.progress.emit(self.index)
        self.finished.emit()

class FetchClipsThread(QThread):
    clips_fetched = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, twitch_api, period_value):
        super().__init__()
        self.twitch_api = twitch_api
        self.period_value = period_value

    def run(self):
        try:
            broadcaster_ids = self.twitch_api.get_live_streamers(language='fr', first=10)
            clips = self.twitch_api.get_top_clips(broadcaster_ids, period=self.period_value, first=10)
            self.clips_fetched.emit(clips)
        except Exception as e:
            self.error_occurred.emit(str(e))