from encryption import *
import socket, hashlib, pickle, time, os, sys
from threading import Thread
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal, QRunnable, Slot)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform, QTextOption, QKeyEvent)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QLayout, QMainWindow, QPushButton,
    QScrollArea, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget, QDialog, QLineEdit, QSpacerItem, QLabel, QStyle, QStyleOption, QComboBox)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 180)
        Form.setStyleSheet("background-color: #202027; color: #999999")
        self.widget = Form
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)

        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Decrypt local data", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Decrypt", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Password", None))
        self.pushButton.clicked.connect(self.decrypt)
        self.pushButton_2.clicked.connect(self.cancel)
    
    def decrypt(self, *args):
        global master_key
        data = self.lineEdit.text().encode()
        if data == b'':
            return
        master_key = import_private_key(main_path + 'secret.pem', data)
        self.widget.close()
    
    def cancel(self, *args):
        sys.exit()


class Ui_Dialog_1(object):
    def setupUi(self, Dialog, main_window):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(350, 180)
        self.dialog = Dialog
        self.dialog.setStyleSheet("background-color: #202027; color: #999999")
        self.main_window = main_window
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 3, 1, 1, 1)

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 1)

        self.comboBox = QComboBox(Dialog)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        layout = self.main_window.verticalLayout_3
        self.dict = {}
        for i in range(layout.count()):
            item = layout.itemAt(i).widget().text()
            self.comboBox.addItem('(' + str(i + 1) + ') ' + item)
        self.pushButton_2.clicked.connect(self.exit)
        self.pushButton.clicked.connect(self.remove_chat)
    
    def remove_chat(self, *args):
        indx = self.comboBox.currentIndex()
        if self.main_window.current_chat != -1:
            current_chat = self.main_window.rooms[self.main_window.current_chat]
            if current_chat == indx:
                self.main_window.current_chat = -1
                self.main_window.clear_chat('')
        os.remove(chats + self.main_window.chats[indx])
        s.send(encrypt(b'EXIT ROOM', server_public))
        self.main_window.reload_chats()
        self.dialog.close()
    
    def exit(self, *args):
        self.dialog.close()


class Ui_Dialog(object):
    def setupUi(self, Dialog, main_window):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        self.dialog = Dialog
        self.dialog.setStyleSheet("background-color: #202027; color: #999999")
        self.main_window = main_window
        Dialog.resize(400, 190)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 2)

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(Dialog)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 0, 0, 1, 2)


        self.retranslateUi()

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self):
        self.dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Room key", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("Dialog", u"Chat name", None))
        self.pushButton.clicked.connect(self.enter_room)
        self.pushButton_2.clicked.connect(self.cancel)

    def enter_room(self, *args):
        if self.lineEdit.text() != '' and self.lineEdit_2.text() != '':
            key = self.lineEdit.text()
        elif self.lineEdit_2.text() != '':
            self.main_window.aes_key = generate_sym_key()
            old_key = self.main_window.key
            s.send(encrypt((b'CREATE ROOM ' + hash(self.main_window.aes_key)), server_public))
            while old_key == self.main_window.key:
                pass
            key = self.main_window.key
        room_id = key.split('::')[0]
        if self.lineEdit_2.text() == '' or os.path.isfile(chats + room_id):
            return
        public = get_public_key(master_key)
        open(chats + room_id, 'wb').write(encrypt((key + '\n' + self.lineEdit_2.text()).encode(), public))
        self.main_window.reload_chats()
        self.dialog.close()
    
    def cancel(self, *args):
        self.dialog.close()


class SignalConnection(QObject):
    messageReceived = Signal(list)
    clearChat = Signal(str)


class ChatUpdater(QRunnable):
    def __init__(self):
        super(ChatUpdater, self).__init__() 
        self.signals = SignalConnection()
    
    def display_message(ls):
        self.messageReceived.emit(ls)
    
    def clear_chat(st):
        self.clearChat.emit(st)


class TextEdit(QTextEdit):
    global myui
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_Return and not event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            myui.send_message()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, username):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1250, 900)
        self.chats = {}
        self.rooms = {}
        self.key = b''
        self.current_chat = -1
        self.events = ChatUpdater()
        self.events.signals.clearChat.connect(self.clear_chat)
        self.events.signals.messageReceived.connect(self.display_message)
        self.username = username
        self.rows = -3
        self.main_window = MainWindow
        self.main_window.setStyleSheet("background-color: #202027; color: #999999")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.formLayout_2 = QFormLayout(self.centralwidget)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setMinimumSize(QSize(250, 0))
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout.addWidget(self.pushButton_3)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 248, 16))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy1)
        self.scrollAreaWidgetContents.setAutoFillBackground(False)
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.formLayout_2.setLayout(0, QFormLayout.LabelRole, self.verticalLayout)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.scrollArea_2 = QScrollArea(self.centralwidget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 976, 776))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_5.addWidget(self.scrollArea_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.textEdit = TextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy2)
        self.textEdit.setMaximumSize(QSize(16777215, 100))

        self.horizontalLayout.addWidget(self.textEdit)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(100, 100))
        font = QFont()
        font.setFamilies([u"Bitstream Charter"])
        font.setPointSize(20)
        font1 = QFont()
        font1.setFamilies([u"Bitstream Charter"])
        font1.setPointSize(13)
        self.font = font1
        self.pushButton_2.setFont(font)

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.verticalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.reload_chats()

        self.scrollArea_2.verticalScrollBar().setVisible(False)

        QMetaObject.connectSlotsByName(MainWindow)

        Thread(target=self.listen_for_messages, daemon=True).start()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Quark", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Add new chat", None))
        self.pushButton.clicked.connect(self.add_chat)
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Remove chat", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u1bd3\u27a4", None))
        self.pushButton_2.clicked.connect(self.send_message)
        self.pushButton_3.clicked.connect(self.remove_chat)

    def send_message(self, *args):
        try:
            global s, current_key
            message = self.textEdit.toPlainText()
            if message == '':
                return
            message = message[:-1]
            s.send(aes_encrypt(current_key, message.encode()))
            self.textEdit.setPlainText('')
        except:
            pass

    def add_chat(self, *args):
        dlg_skeleton = QDialog(self.main_window)
        dlg = Ui_Dialog()
        dlg.setupUi(dlg_skeleton, self)
        dlg_skeleton.exec()
    
    @Slot(str)
    def clear_chat(self, st):
        layout = self.gridLayout_2
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)
    
    def enter_chat(self, fullkey, current_chat, *args):
        global link
        link = fullkey
        self.current_chat = current_chat
        try:
            global s, current_key
            self.events.signals.clearChat.emit('')
            room_id, key = fullkey.split('::')[0], unhexlify(fullkey.split('::')[1].encode())
            s.send(encrypt(b'ENTER ROOM ' + room_id.encode() + b' ' + hash(key), server_public))
        except Exception as e:
            pass
    
    def remove_chat(self):
        dlg_skeleton = QDialog(self.main_window)
        dlg = Ui_Dialog_1()
        dlg.setupUi(dlg_skeleton, self)
        dlg_skeleton.exec()
    
    def add_button(self, key, number, name):
        room_id = key.split('::')[0]
        self.chats[number] = room_id
        self.rooms[room_id] = number
        new_chat = QPushButton(text=name)
        new_chat.clicked.connect(lambda: self.enter_chat(key, room_id))
        self.verticalLayout_3.addWidget(new_chat)
    
    def reload_chats(self):
        self.chats = {}
        self.rooms = {}
        layout = self.verticalLayout_3
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)
        ls = os.listdir(chats)
        number = 0
        for file in ls:
            key, name = decrypt(open(chats + file, 'rb').read(), master_key).decode().split('\n')
            self.add_button(key, number, name)
            number += 1

    def listen_for_messages(self, *args):
        global s, current_key, link, room_id
        while True:
            try:
                data = s.recv(47960)
                ls = pickle.loads(data)
                if len(ls) == 3:
                    username, msg, datetime = ls
                    username = decrypt(username, private_key).decode()
                    msg = aes_decrypt(current_key, msg).decode()
                    datetime = decrypt(datetime, private_key).decode()
                    if username != self.username:
                        self.events.signals.messageReceived.emit([username, msg, 0, datetime])
                        continue
                    self.events.signals.messageReceived.emit([username, msg, 1, datetime])
                else:
                    msg = decrypt(ls[0], private_key).decode()
                    if msg == "Login successful!":
                        self.events.signals.messageReceived.emit(['SERVER', 'Entered a new room.\nRoom key: ' + link, 0, 'system notifications'])
                        fullkey = link
                        room_id, current_key = fullkey.split('::')[0], unhexlify(fullkey.split('::')[1].encode())
                    elif msg == "Login attempt failed. Incorrect password or room key!":
                        continue
                    else:
                        self.events.signals.messageReceived.emit(['SERVER', msg, 0, 'system notifications'])
            except Exception as e:
                try:
                    room_id = decrypt(data, private_key).decode()
                    self.key = room_id + '::' + hexlify(self.aes_key).decode()
                except Exception as e:
                    pass
    
    @Slot(list)
    def display_message(self, ls):
        scrollbar = self.scrollArea_2.verticalScrollBar()
        scvalue = scrollbar.value()
        scmax = scrollbar.maximum()
        user, text, side, dtime = ls
        self.rows += 3
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        message = QTextEdit(text=text)
        message.document().setTextWidth(message.viewport().width())
        margins = message.contentsMargins()
        height = int(message.document().size().height() + margins.top() + margins.bottom())
        message.setFixedHeight(height)
        message.setReadOnly(True)
        message.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)
        message_widget = QWidget()
        message_layout = QHBoxLayout()
        message_widget.setLayout(message_layout)
        message_layout.addWidget(message)
        message_layout.setContentsMargins(0, 0, 0, 0)
        username = QLabel(text=f' {user} ')
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        username.setSizePolicy(sizePolicy2)
        username_widget = QWidget()
        username_layout = QHBoxLayout()
        username_widget.setLayout(username_layout)
        username.setStyleSheet('font-size: 15px; color: #FFFFFF; background-color: #27272E; border-radius: 2px')
        username_layout.addWidget(username)
        username_layout.setContentsMargins(0, 0, 0, 0)
        time = QLabel(text=f' {dtime} ')
        time.setSizePolicy(sizePolicy2)
        time_widget = QWidget()
        time_layout = QHBoxLayout()
        time_widget.setLayout(time_layout)
        time.setStyleSheet('font-size: 15px; color: #FFFFFF')
        time_layout.addWidget(time)
        time_layout.setContentsMargins(0, 0, 0, 0)
        message.setStyleSheet('background-color: #303037; border-radius: 2px')
        message.setSizePolicy(sizePolicy)
        message_widget.setSizePolicy(sizePolicy)
        spacer = QLabel(text='')
        spacer.setSizePolicy(sizePolicy)
        message.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        message.setFont(self.font)
        if side == 1:
            username_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            time_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.gridLayout_2.addWidget(username_widget, self.rows, 1)
            self.gridLayout_2.addWidget(message_widget, self.rows + 1, 1)
            self.gridLayout_2.addWidget(spacer, self.rows + 1, 0)
            self.gridLayout_2.addWidget(time, self.rows + 2, 1)
        else:
            username_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            time_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.gridLayout_2.addWidget(username_widget, self.rows, 0)
            self.gridLayout_2.addWidget(message_widget, self.rows + 1, 0)
            self.gridLayout_2.addWidget(spacer, self.rows + 1, 1)
            self.gridLayout_2.addWidget(time, self.rows + 2, 0)
        if scvalue == scmax:
            scrollbar.setMaximum(scmax + height + 80)
            scrollbar.setValue(scmax + height + 80)


if sys.platform in ['win32', 'MSYS2', 'cygwin']:
    main_path = f'{os.environ["USERPROFILE"]}\\ProgramFiles\\Quark\\'
    chats = main_path + 'Chats\\'
else:
    main_path = f'/home/{os.environ["USER"]}/Quark/'
    chats = main_path + 'Chats/'

master_key = b''

app = QApplication()
new_widget = QWidget()
decryption = Ui_Form()
decryption.setupUi(new_widget)
new_widget.show()
app.exec()

host, port, login, password, reg_code = decrypt(open(main_path + 'config', 'rb').read(), master_key).decode().split('\n')
port = int(port)

s = socket.socket()
s.connect((host, port))

server_public = import_public_key(s.recv(3072))
private_key = generate_private_key()
public_pem = export_public_key(get_public_key(private_key))
s.send(public_pem)
decrypt(s.recv(3072), private_key).decode()


def authorize(reg_code, login, password):
    s.send(encrypt(f'{reg_code} {login} {hash(password.encode()).decode()}'.encode(), server_public))
    status = decrypt(pickle.loads(s.recv(3072))[0], private_key).decode()
    if status == "Reg code incorrect!":
        return False
    return True


def main():
    global s, server_public, private_key, login, myui
    current_key = None

    main_window = QMainWindow()
    myui = Ui_MainWindow()
    myui.setupUi(main_window, login)
    main_window.show()
    app.exec()


if authorize(reg_code, login, password):
    main()
