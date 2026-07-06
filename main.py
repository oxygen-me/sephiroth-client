import sys
import resources_rc
import requests
from installer import SephirothInstaller
from PySide6.QtCore import Qt, QUrl, Signal, QThread
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QStackedWidget, QPushButton, QHBoxLayout, \
    QFrame, QComboBox, QFileDialog, QLineEdit, QProgressBar, QCheckBox, QMessageBox
import os

edition0 = "[1] Basic"
install_location = r"C:\Program Files\Sephiroth"
global_version = "err"

url = f"https://api.github.com/repos/oxygen-me/SephirothOS-v2/releases/latest"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    global_version = data["tag_name"]
    print(global_version)
else:
    print(f"Error: Unable to retrieve latest release (Status Code: {response.status_code})")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SephirothOS Installer")
        self.resize(600, 0)

        self.audio = QAudioOutput()
        self.player = QMediaPlayer()

        self.player.setAudioOutput(self.audio)
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.audio.setVolume(0.3)

        self.player.setSource(QUrl("qrc:/assets/InstallerMusic.mp3"))
        self.player.play()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()

        self.stack.addWidget(WelcomePage(self.stack))
        self.stack.addWidget(EditionPage(self.stack))
        self.stack.addWidget(PathPage(self.stack))
        self.stack.addWidget(ReadyPage(self.stack))
        self.stack.addWidget(InstallPage(self.stack))
        self.stack.addWidget(DonePage(self.stack))

        self.layout.addWidget(self.stack)

        self.stack.setCurrentIndex(0)

class WelcomePage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(0)

        self.title = QLabel("SephirothOS")
        self.title.setStyleSheet("background-color: transparent; font-family: Segoe UI; font-size: 56px; font-weight: 800; font-style: italic;")
        self.mainlayout.addWidget(self.title)

        self.subtitle = QLabel("Welcome back to your despair.")
        self.subtitle.setStyleSheet("background-color: transparent; font-family: Segoe UI; font-size: 16px; font-weight: 400; font-style: italic;")
        self.mainlayout.addWidget(self.subtitle)
        self.mainlayout.addSpacing(20)

        self.div = QFrame()
        self.div.setFrameShape(QFrame.Shape.HLine)
        self.div.setFrameShadow(QFrame.Shadow.Sunken)
        self.div.setFixedHeight(4)
        self.mainlayout.addWidget(self.div)
        self.mainlayout.addSpacing(20)

        self.btnlayout = QHBoxLayout()
        self.btnlayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.nextbtn = QPushButton("Next")
        self.nextbtn.setStyleSheet("""
        QPushButton {
        background-color: #496f91;
        color: white;
        font-family: Segoe UI;
        font-size: 14px;
        font-weight: 600;
        padding: 4px 20px;
        }
        QPushButton:hover {
        background-color: #5b82a3;
        }
        QPushButton:pressed {
        background-color: #36526b
        }""")
        self.nextbtn.clicked.connect(self.next_page)
        self.btnlayout.addWidget(self.nextbtn)

        self.mainlayout.addStretch()

        self.mainlayout.addLayout(self.btnlayout)
        self.setLayout(self.mainlayout)

    def next_page(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)

    def last_page(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() - 1)

class EditionPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        self.editions = {
            "[1] Basic": "Basic Edition includes all of the essential features for your Sephiroth experience. Made by Doctor Cloud Strife.",
            "[2] Workplace": "Sephiroth wears a fucking suit 8 hours a day, 5 days a week. Wall Street's calling, bitch.",
            "[3] Premium": "Premium Edition brings a very premium experience to the table. One could even call it a premium edition.",
            "[4] Ultimate": "55 burgers, 55 fries, 55 tacos, 55 pies, 55 cokes, 100 tater tots, 100 pizzas, 100 tenders, 100 meatballs, 100 coffees, 55 wings, 55 shakes, 55 pancakes, 55 pastas, 55 peppers, and 155 taters."
        }

        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(0)

        self.title = QLabel("Choose an Edition")
        self.title.setStyleSheet("background-color: transparent; font-family: Segoe UI; font-size: 36px; font-weight: 800; font-style: italic;")
        self.mainlayout.addWidget(self.title)
        self.mainlayout.addSpacing(10)

        self.div = QFrame()
        self.div.setFrameShape(QFrame.Shape.HLine)
        self.div.setFrameShadow(QFrame.Shadow.Sunken)
        self.div.setFixedHeight(4)
        self.mainlayout.addWidget(self.div)
        self.mainlayout.addSpacing(10)

        self.selectlayout = QHBoxLayout()
        self.selectvlayout = QVBoxLayout()


        self.selecter = QComboBox()
        self.selecter.setStyleSheet("font-family: Segoe UI;")
        self.selecter.addItems(["[1] Basic", "[2] Workplace", "[3] Premium", "[4] Ultimate"])
        self.selectvlayout.addWidget(self.selecter)

        self.selectvlayout.addStretch()

        self.selectlayout.addLayout(self.selectvlayout)

        self.selectlayout.addSpacing(20)

        self.description = QLabel()
        self.description.setStyleSheet("font-family: Segoe UI; font-size: 16px; padding: 0px 0px")
        self.description.setWordWrap(True)
        self.description.setText(self.editions[self.selecter.currentText()])
        self.selectlayout.addWidget(self.description)

        self.selecter.currentTextChanged.connect(self.update_description)


        self.btnlayout = QHBoxLayout()

        self.backbtn = QPushButton("Back")
        self.backbtn.setStyleSheet("""
                QPushButton {
                background-color: #496f91;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
                font-weight: 600;
                padding: 4px 20px;
                }
                QPushButton:hover {
                background-color: #5b82a3;
                }
                QPushButton:pressed {
                background-color: #36526bdd
                }""")
        self.backbtn.clicked.connect(self.last_page)
        self.btnlayout.addWidget(self.backbtn)

        self.btnlayout.addStretch()

        self.nextbtn = QPushButton("Next")
        self.nextbtn.setStyleSheet("""
        QPushButton {
        background-color: #496f91;
        color: white;
        font-family: Segoe UI;
        font-size: 14px;
        font-weight: 600;
        padding: 4px 20px;
        }
        QPushButton:hover {
        background-color: #5b82a3;
        }
        QPushButton:pressed {
        background-color: #36526b
        }""")
        self.nextbtn.clicked.connect(self.next_page)
        self.btnlayout.addWidget(self.nextbtn)

        self.mainlayout.addLayout(self.selectlayout)

        self.mainlayout.addStretch()

        self.mainlayout.addLayout(self.btnlayout)
        self.setLayout(self.mainlayout)

    def update_description(self, edition):
        self.description.setText(self.editions[edition])
        global edition0
        edition0 = self.selecter.currentText()

    def next_page(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)

    def last_page(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() - 1)

class PathPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(0)

        self.title = QLabel("Install Location")
        self.title.setStyleSheet("background-color: transparent; font-family: Segoe UI; font-size: 36px; font-weight: 800; font-style: italic;")
        self.mainlayout.addWidget(self.title)

        self.subtitle = QLabel("The installer will create the directory if it doesn't exist.")
        self.subtitle.setStyleSheet("background-color: transparent; font-family: Segoe UI; font-size: 16px; font-weight: 400; font-style: italic;")
        self.mainlayout.addWidget(self.subtitle)
        self.mainlayout.addSpacing(10)

        self.div = QFrame()
        self.div.setFrameShape(QFrame.Shape.HLine)
        self.div.setFrameShadow(QFrame.Shadow.Sunken)
        self.div.setFixedHeight(4)
        self.mainlayout.addWidget(self.div)
        self.mainlayout.addSpacing(10)

        self.path = QLineEdit(r"C:\Program Files\Sephiroth")
        self.path.textChanged.connect(self.set_path)

        self.browse = QPushButton("Browse...")
        self.browse.clicked.connect(self.select_folder)

        layout = QHBoxLayout()
        layout.addWidget(self.path)
        layout.addWidget(self.browse)

        self.mainlayout.addLayout(layout)

        self.btnlayout = QHBoxLayout()
        self.btnlayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.backbtn = QPushButton("Back")
        self.backbtn.setStyleSheet("""
                        QPushButton {
                        background-color: #496f91;
                        color: white;
                        font-family: Segoe UI;
                        font-size: 14px;
                        font-weight: 600;
                        padding: 4px 20px;
                        }
                        QPushButton:hover {
                        background-color: #5b82a3;
                        }
                        QPushButton:pressed {
                        background-color: #36526bdd
                        }""")
        self.backbtn.clicked.connect(self.last_page)
        self.btnlayout.addWidget(self.backbtn)

        self.btnlayout.addStretch()

        self.nextbtn = QPushButton("Next")
        self.nextbtn.setStyleSheet("""
        QPushButton {
        background-color: #496f91;
        color: white;
        font-family: Segoe UI;
        font-size: 14px;
        font-weight: 600;
        padding: 4px 20px;
        }
        QPushButton:hover {
        background-color: #5b82a3;
        }
        QPushButton:pressed {
        background-color: #36526b
        }""")
        self.nextbtn.clicked.connect(self.next_page)
        self.btnlayout.addWidget(self.nextbtn)

        self.mainlayout.addStretch()

        self.mainlayout.addLayout(self.btnlayout)
        self.setLayout(self.mainlayout)

    def next_page(self):
        next_index = self.stack.currentIndex() + 1

        if next_index == 3:
            self.stack.widget(3).update_info()

        self.stack.setCurrentIndex(next_index)

    def last_page(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() - 1)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Choose installation folder",
            self.path.text()
        )

        if folder:
            self.path.setText(folder)

    def set_path(self):
        global install_location
        install_location = self.path.text()

class ReadyPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(0)

        self.title = QLabel("Ready to Install?")
        self.title.setStyleSheet("background-color: transparent; font-family: Segoe UI; font-size: 36px; font-weight: 800; font-style: italic;")
        self.mainlayout.addWidget(self.title)

        self.subtitle = QLabel("We put all your shit here so you can double-check.")
        self.subtitle.setStyleSheet("background-color: transparent; font-family: Segoe UI; font-size: 16px; font-weight: 400; font-style: italic;")
        self.mainlayout.addWidget(self.subtitle)
        self.mainlayout.addSpacing(10)

        self.div = QFrame()
        self.div.setFrameShape(QFrame.Shape.HLine)
        self.div.setFrameShadow(QFrame.Shadow.Sunken)
        self.div.setFixedHeight(4)
        self.mainlayout.addWidget(self.div)
        self.mainlayout.addSpacing(10)

        self.pathlabel = QLabel()
        self.editionlabel = QLabel()
        self.versionlabel = QLabel()

        self.pathlabel.setStyleSheet("font-family: Segoe UI; font-size: 16px; font-weight: 500;")
        self.editionlabel.setStyleSheet("font-family: Segoe UI; font-size: 16px; font-weight: 500;")
        self.versionlabel.setStyleSheet("font-family: Segoe UI; font-size: 16px; font-weight: 500;")

        self.mainlayout.addWidget(self.pathlabel)
        self.mainlayout.addWidget(self.editionlabel)
        self.mainlayout.addWidget(self.versionlabel)

        self.update_info()

        self.btnlayout = QHBoxLayout()
        self.btnlayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.backbtn = QPushButton("Back")
        self.backbtn.setStyleSheet("""
                        QPushButton {
                        background-color: #496f91;
                        color: white;
                        font-family: Segoe UI;
                        font-size: 14px;
                        font-weight: 600;
                        padding: 4px 20px;
                        }
                        QPushButton:hover {
                        background-color: #5b82a3;
                        }
                        QPushButton:pressed {
                        background-color: #36526bdd
                        }""")
        self.backbtn.clicked.connect(self.last_page)
        self.btnlayout.addWidget(self.backbtn)

        self.btnlayout.addStretch()

        self.nextbtn = QPushButton("Install")
        self.nextbtn.setStyleSheet("""
        QPushButton {
        background-color: #496f91;
        color: white;
        font-family: Segoe UI;
        font-size: 14px;
        font-weight: 600;
        padding: 4px 20px;
        }
        QPushButton:hover {
        background-color: #5b82a3;
        }
        QPushButton:pressed {
        background-color: #36526b
        }""")
        self.nextbtn.clicked.connect(self.next_page)
        self.btnlayout.addWidget(self.nextbtn)

        self.mainlayout.addStretch()

        self.mainlayout.addLayout(self.btnlayout)
        self.setLayout(self.mainlayout)

    def next_page(self):
        if os.path.isdir(install_location):
            reply = QMessageBox.warning(
                self, "Installation Found",
                                "An installation of SephirothOS already exists at the target path. Are you sure you want to proceed?",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
                                QMessageBox.StandardButton.Cancel
                                )

            if reply == QMessageBox.StandardButton.Yes:
                install_page = self.stack.widget(4)
                self.stack.setCurrentIndex(4)
                install_page.start_install()
        else:
            install_page = self.stack.widget(4)
            self.stack.setCurrentIndex(4)
            install_page.start_install()

    def last_page(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() - 1)

    def update_info(self):
        self.pathlabel.setText("Installing to: " + install_location)
        self.editionlabel.setText("Selected Edition: " + edition0)
        self.versionlabel.setText("Version to Install: " + global_version)

class InstallPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(0)

        self.title = QLabel("Installing...")
        self.title.setStyleSheet("background-color: transparent; font-family: Segoe UI; font-size: 36px; font-weight: 800; font-style: italic;")
        self.mainlayout.addWidget(self.title)
        self.mainlayout.addSpacing(10)

        self.div = QFrame()
        self.div.setFrameShape(QFrame.Shape.HLine)
        self.div.setFrameShadow(QFrame.Shadow.Sunken)
        self.div.setFixedHeight(4)
        self.mainlayout.addWidget(self.div)
        self.mainlayout.addSpacing(20)

        self.status = QLabel("Preparing installer...")
        self.status.setStyleSheet(
            "font-family: Segoe UI;"
            "font-size: 16px;"
        )
        self.mainlayout.addWidget(self.status)

        self.mainlayout.addSpacing(10)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.mainlayout.addWidget(self.progress)

        self.mainlayout.addStretch()

        self.setLayout(self.mainlayout)

    def start_install(self):
        self.thread = InstallThread(install_location)

        self.thread.progress.connect(
            self.update_progress
        )

        self.thread.finished.connect(
            self.install_finished
        )

        self.thread.start()

    def update_progress(self, value, text):
        self.progress.setValue(value)
        self.status.setText(text)

    def install_finished(self):
        self.progress.setValue(100)
        self.status.setText("Installation complete!")
        self.stack.setCurrentIndex(5)

class InstallThread(QThread):

    progress = Signal(int, str)

    def __init__(self, install_path):
        super().__init__()
        self.install_path = install_path

    def run(self):
        installer = SephirothInstaller(
            edition0,
            self.install_path,
            self.progress.emit
        )

        installer.install()

class DonePage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        self.mainlayout = QVBoxLayout()
        self.mainlayout.setContentsMargins(20, 20, 20, 20)
        self.mainlayout.setSpacing(0)

        self.title = QLabel("Complete")
        self.title.setStyleSheet("background-color: transparent; font-family: Segoe UI; font-size: 36px; font-weight: 800; font-style: italic;")
        self.mainlayout.addWidget(self.title)

        self.subtitle = QLabel("Fuck you and have a nice day.")
        self.subtitle.setStyleSheet(
            "background-color: transparent; font-family: Segoe UI; font-size: 16px; font-weight: 400; font-style: italic;")
        self.mainlayout.addWidget(self.subtitle)
        self.mainlayout.addSpacing(10)

        self.div = QFrame()
        self.div.setFrameShape(QFrame.Shape.HLine)
        self.div.setFrameShadow(QFrame.Shadow.Sunken)
        self.div.setFixedHeight(4)
        self.mainlayout.addWidget(self.div)
        self.mainlayout.addSpacing(10)

        self.shortcut = QCheckBox("Create Desktop Shortcut")
        self.launch = QCheckBox("Launch SephirothOS")
        self.startmenu = QCheckBox("Create Start Menu Shortcut")

        self.shortcut.setChecked(False)
        self.launch.setChecked(True)
        self.startmenu.setChecked(True)

        self.mainlayout.addWidget(self.launch)
        self.mainlayout.addWidget(self.startmenu)
        self.mainlayout.addWidget(self.shortcut)

        self.btnlayout = QHBoxLayout()
        self.btnlayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.nextbtn = QPushButton("Finish")
        self.nextbtn.setStyleSheet("""
                QPushButton {
                background-color: #496f91;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
                font-weight: 600;
                padding: 4px 20px;
                }
                QPushButton:hover {
                background-color: #5b82a3;
                }
                QPushButton:pressed {
                background-color: #36526b
                }""")
        self.nextbtn.clicked.connect(self.finish)
        self.btnlayout.addWidget(self.nextbtn)

        self.mainlayout.addStretch()

        self.mainlayout.addLayout(self.btnlayout)

        self.setLayout(self.mainlayout)

    def finish(self):
        installer = SephirothInstaller(edition0, install_location)

        if self.shortcut.isChecked():
            installer.create_shortcut()

        if self.launch.isChecked():
            installer.launch_app()

        if self.startmenu.isChecked():
            installer.start_shortcut()

        QApplication.quit()
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())