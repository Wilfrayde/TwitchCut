import sys
from PyQt5.QtWidgets import QApplication
from src.gui import TwitchToTikTokGUI  # Ajustez l'importation pour inclure le chemin 'src'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = TwitchToTikTokGUI()
    gui.show()
    sys.exit(app.exec_())