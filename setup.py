from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QWidget)
from encryption import *
import sys, os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(763, 366)
        MainWindow.setStyleSheet("background-color: #202027; color: #999999")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_4 = QLineEdit(self.centralwidget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.gridLayout.addWidget(self.lineEdit_4, 1, 1, 1, 1)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 7, 0, 1, 1)

        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.gridLayout.addWidget(self.lineEdit_3, 1, 0, 1, 1)

        self.lineEdit_6 = QLineEdit(self.centralwidget)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.gridLayout.addWidget(self.lineEdit_6, 0, 1, 1, 1)

        self.lineEdit_5 = QLineEdit(self.centralwidget)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.gridLayout.addWidget(self.lineEdit_5, 2, 1, 1, 1)

        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 2, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 7, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Server IP", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Setup", None))
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.lineEdit_6.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Server port", None))
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Encryption passphrase", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Authentification code", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.pushButton.clicked.connect(self.setup)
        self.pushButton_2.clicked.connect(self.cancel)

    def setup(self, *args):
        host = self.lineEdit.text()
        port = self.lineEdit_6.text()
        login = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        reg_code = self.lineEdit_2.text()
        passphrase = self.lineEdit_5.text()
        if host == '' or port == '' or login == '' or password == '' or reg_code == '' or passphrase == '':
            return
        data = host + '\n' + port + '\n' + login + '\n' + password + '\n' + reg_code
        prkey = generate_private_key()
        pukey = get_public_key(prkey)
        data = encrypt(data.encode(), pukey)
        open(main_path + 'config', 'wb').write(data)
        open(main_path + 'secret.pem', 'wb').write(export_private_key(prkey, passphrase.encode()))
        app.exit()
    
    def cancel(self, *args):
        app.exit()


if sys.platform in ['win32', 'MSYS2', 'cygwin']:
    main_path = f'{os.environ["USERPROFILE"]}\\AppData\\Local\\Quark\\'
    chats = main_path + 'Chats\\'
else:
    main_path = f'/home/{os.environ["USER"]}/Quark/'
    chats = main_path + 'Chats/'

if not os.path.isdir(main_path):
    os.mkdir(main_path)
if not os.path.isdir(chats):
    os.mkdir(chats)

app = QApplication()
main_window = QMainWindow()
myui = Ui_MainWindow()
myui.setupUi(main_window)
main_window.show()
app.exec()
