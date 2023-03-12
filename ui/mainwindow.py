from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from functools import partial

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QListWidgetItem, QMenu, QAction

from player.Player import Player
from ui.NameChooserDialog import NameChooserDialog

class ClickableWidget(QtWidgets.QWidget):
    clicked = pyqtSignal()
    data = ''

    def __init__(self, parent=None):
        super(ClickableWidget, self).__init__(parent=parent)

    def mousePressEvent(self, event):
        self.clicked.emit()

    def setUserData(self, d):
        self.data = d

    def getUserData(self):
        return self.data

    def enterEvent(self, event):
        # Acción a realizar cuando el mouse entra en las coordenadas del widget
        self.setStyleSheet('background-color:black;')

        for widget in self.findChildren(QtWidgets.QWidget):
            widget.setStyleSheet('background-color:black;')

    def leaveEvent(self, event):
        # Acción a realizar cuando el mouse entra en las coordenadas del widget
        self.setStyleSheet('background-color:none;')

        for widget in self.findChildren(QtWidgets.QWidget):
            widget.setStyleSheet('background-color:none;')


class Ui_MainWindow(object):

    # Se actualiza el frame de las canciones dependiendo de la lista seleccionada
    def select_list(self, list_name):
        content = self.player.get_playlist_content(list_name)
        self.songsList.clear()

        for data in content:
            self.add_song_to_frame(data.split('||')[1] + ' (' + data.split('||')[2] + ')', data)
        self.is_playlist_showing = True
        self.showing_favourites = False
        self.playlist_name = list_name

    # Se crea una nueva lista
    def new_list(self, add=None):
        nombres_ocupados = self.player.get_playlists()
        name = NameChooserDialog().exec_()
        if (len(name.strip()) == 0 or name.isspace()):
            name = 'Nueva Lista'

        # Controlamos que no existan nombres de playlists duplicados para evitar errores
        valido = False
        cont = 0
        aux = name
        while (not valido):
            if aux in nombres_ocupados:
                cont = cont + 1
                aux = name + '(' + str(cont) + ')'
            else:
                valido = True
        name = aux

        self.player.guardar_playlist(name)
        if add is not  False:
            self.player.añadir_cancion(name, add)
        self.add_list(name)

    # Se añade un objeto al frame de las listas de reproducción
    def add_list(self, name):

        Item = ClickableWidget(self.listsContainer)
        Item.setMinimumSize(QtCore.QSize(0, 40))
        Item.setMaximumSize(QtCore.QSize(16777215, 40))
        Item.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        Item.setObjectName("playListItem")
        hLayout = QtWidgets.QHBoxLayout(Item)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.setObjectName("horizontalLayout_2")
        hLayout.setSpacing(0)
        Icon = QtWidgets.QPushButton(Item)
        Icon.setMinimumSize(QtCore.QSize(40, 40))
        Icon.setMaximumSize(QtCore.QSize(40, 40))
        Icon.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/lista-de-verificacion.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        Icon.setIcon(icon2)
        Icon.setObjectName("listIcon")
        hLayout.addWidget(Icon)
        NameLabel = QtWidgets.QLabel(Item)
        font = QtGui.QFont()
        font.setPointSize(10)
        NameLabel.setFont(font)
        NameLabel.setObjectName("listNameLabel")
        NameLabel.setStyleSheet('background-color:none;')
        NameLabel.setText(name)
        hLayout.addWidget(NameLabel)
        startPlayList = QtWidgets.QPushButton(Item)
        startPlayList.setMinimumSize(QtCore.QSize(40, 40))
        startPlayList.setMaximumSize(QtCore.QSize(40, 40))
        startPlayList.setText("")

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/boton-de-play.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        startPlayList.setIcon(icon3)
        startPlayList.setObjectName("startPlayList")
        startPlayList.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        startPlayList.clicked.connect(partial(self.player.reproducir_playlist, name))
        startPlayList.clicked.connect(partial(self.select_list, name))
        hLayout.addWidget(startPlayList)
        self.verticalLayout_3.addWidget(Item)
        Item.clicked.connect(partial(self.select_list, name))
        Item.setContextMenuPolicy(Qt.CustomContextMenu)
        Item.customContextMenuRequested.connect(partial(self.show_playlist_context_menu, Item, name))
        Item.setUserData(self.player.get_playlist_content(name))


    # Se define la apariencia de la ventana y se conectan las señales a sus slots correspondientes
    def setupUi(self, MainWindow):
        self.player = Player()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1028, 755)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 700))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow{\n"
                                 "\n"
                                 "}\n"
                                 "\n"
                                 "#songsFrame{\n"
                                 "    border:1px solid white;\n"
                                 "}\n"
                                 "\n"
                                 "#playListFrame{\n"
                                 "    border:1px solid white;\n"
                                 "}\n"
                                 "\n"
                                 "#playListBox{\n"
                                 "    border:none;\n"
                                 "}\n"
                                 "\n"
                                 "QFrame#container{\n"
                                 "    background-color:#2F2C2C;\n"
                                 "}\n"
                                 "QFrame#menu{\n"
                                 "    background-color:rgb(0, 66, 200);\n"
                                 "}\n"
                                 "\n"
                                 "QFrame#reproduciendoFrame{\n"
                                 "    background-color:black;\n"
                                 "}\n"
                                 "\n"
                                 "QLineEdit#searchText{\n"
                                 "    border:1px solid white;\n"
                                 "    border-radius:20px;\n"
                                 "    text-align:center;\n"
                                 "    padding-left:20px;\n"
                                 "    padding-right:20px;\n"
                                 "    background-color:rgb(0, 66, 200);\n"
                                 "    color:white;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton{\n"
                                 "    background-color:rgb(0, 66, 200);\n"
                                 "    border:none;\n"
                                 "    color:white;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton#addList{\n"
                                 "    background:none;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:hover{\n"
                                 "    background-color:rgb(0, 50, 150);\n"
                                 "}\n"
                                 "\n"
                                 "QGroupBox#playListBox{\n"
                                 "    color:white;\n"
                                 "    border-top:;\n"
                                 "}\n"
                                 "\n"
                                 "QLabel#listsLabel{\n"
                                 "    color:white;\n"
                                 "}"
                                 "ClickableWidget:hover{\n"
                                 "    background-color:black;\n"
                                 "}"
                                 )
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks | QtWidgets.QMainWindow.AnimatedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.container = QtWidgets.QFrame(self.centralwidget)
        self.container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.container.setLineWidth(0)
        self.container.setObjectName("container")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.container)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.menu = QtWidgets.QFrame(self.container)
        self.menu.setMinimumSize(QtCore.QSize(0, 60))
        self.menu.setMaximumSize(QtCore.QSize(16777215, 60))
        self.menu.setStyleSheet("QFrame#menu{\n"
                                "    border-bottom-left-radius:30px;\n"
                                "    border-bottom-right-radius:30px;\n"
                                "}")
        self.menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menu.setObjectName("menu")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.menu)
        self.horizontalLayout.setContentsMargins(30, 0, 30, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mostListenedBtn = QtWidgets.QPushButton(self.menu)
        self.mostListenedBtn.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setFamily("Microsoft New Tai Lue")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.mostListenedBtn.setFont(font)
        self.mostListenedBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mostListenedBtn.setObjectName("mostListenedBtn")
        self.mostListenedBtn.clicked.connect(self.most_listened_action)
        self.horizontalLayout.addWidget(self.mostListenedBtn)
        self.favoritasBtn = QtWidgets.QPushButton(self.menu)
        self.favoritasBtn.setMinimumSize(QtCore.QSize(0, 60))
        self.favoritasBtn.clicked.connect(self.favourites_action)
        font = QtGui.QFont()
        font.setFamily("Microsoft New Tai Lue")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.favoritasBtn.setFont(font)
        self.favoritasBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.favoritasBtn.setObjectName("favoritasBtn")
        self.horizontalLayout.addWidget(self.favoritasBtn)
        self.searchText = QtWidgets.QLineEdit(self.menu)
        self.searchText.setMinimumSize(QtCore.QSize(0, 40))
        self.searchText.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI Light")
        font.setPointSize(11)
        self.searchText.setFont(font)
        self.searchText.setObjectName("searchText")
        self.searchText.editingFinished.connect(self.search_songs)
        self.horizontalLayout.addWidget(self.searchText)
        self.verticalLayout_2.addWidget(self.menu)
        self.frame = QtWidgets.QFrame(self.container)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.playListFrame = QtWidgets.QFrame(self.frame)
        self.playListFrame.setMaximumSize(QtCore.QSize(500, 16777215))
        self.playListFrame.setStyleSheet("*{\n"
                                         "    color:white;\n"
                                         "    background-color:#2F2C2C;\n"
                                         "}\n"
                                         "QPushButton{\n"
                                         "    background:none;\n"
                                         "}\n"
                                         "\n"
                                         "QLabel{\n"
                                         "    color:white;\n"
                                         "}")
        self.playListFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.playListFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.playListFrame.setObjectName("playListFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.playListFrame)
        self.verticalLayout_4.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_2 = QtWidgets.QFrame(self.playListFrame)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.listsLabel = QtWidgets.QLabel(self.frame_2)
        self.listsLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.listsLabel.setFont(font)
        self.listsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.listsLabel.setObjectName("listsLabel")
        self.horizontalLayout_3.addWidget(self.listsLabel)
        self.addList = QtWidgets.QPushButton(self.frame_2)
        self.addList.setMinimumSize(QtCore.QSize(40, 40))
        self.addList.setMaximumSize(QtCore.QSize(40, 40))
        self.addList.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addList.setText("")
        self.addList.clicked.connect(self.new_list)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/anadir-lista (1).png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.addList.setIcon(icon1)
        self.addList.setObjectName("addList")
        self.horizontalLayout_3.addWidget(self.addList)
        self.verticalLayout_4.addWidget(self.frame_2)
        self.listsScroll = QtWidgets.QScrollArea(self.playListFrame)
        self.listsScroll.setWidgetResizable(True)
        self.listsScroll.setObjectName("listsScroll")
        self.scrollContents = QtWidgets.QWidget()
        self.scrollContents.setGeometry(QtCore.QRect(0, 0, 496, 514))
        self.scrollContents.setStyleSheet("")
        self.scrollContents.setObjectName("scrollContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollContents)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.listsContainer = QtWidgets.QFrame(self.scrollContents)
        self.listsContainer.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setKerning(True)
        self.listsContainer.setFont(font)
        self.listsContainer.setStyleSheet("")
        self.listsContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listsContainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.listsContainer.setObjectName("listsContainer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.listsContainer)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.listsContainer, 0, 0, 1, 1)
        self.listsScroll.setWidget(self.scrollContents)
        self.verticalLayout_4.addWidget(self.listsScroll)
        self.listsScroll.raise_()
        self.frame_2.raise_()
        self.horizontalLayout_5.addWidget(self.playListFrame)
        self.songsFrame = QtWidgets.QFrame(self.frame)
        self.songsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.songsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.songsFrame.setObjectName("songsFrame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.songsFrame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.songsList = QtWidgets.QListWidget(self.songsFrame)
        self.songsList.setStyleSheet("background-color:rgb(47, 44, 44);\n"
                                     "color:white;\n"
                                     "border:none;")
        self.songsList.setObjectName("songsList")
        self.songsList.itemClicked.connect(self.song_selected)
        self.songsList.activated.connect(self.song_selected)
        self.songsList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.songsList.customContextMenuRequested.connect(self.show_song_context_menu)
        self.gridLayout_3.addWidget(self.songsList, 0, 0, 1, 1)
        self.horizontalLayout_5.addWidget(self.songsFrame)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.verticalLayout_2.addWidget(self.frame)
        self.reproduciendoFrame = QtWidgets.QFrame(self.container)
        self.reproduciendoFrame.setMinimumSize(QtCore.QSize(0, 80))
        self.reproduciendoFrame.setMaximumSize(QtCore.QSize(16777215, 80))
        self.reproduciendoFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.reproduciendoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.reproduciendoFrame.setObjectName("reproduciendoFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.reproduciendoFrame)
        self.horizontalLayout_2.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.reproduciendoFrame)
        self.frame_4.setStyleSheet("color:white;")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.labelTitulo = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitulo.setFont(font)
        self.labelTitulo.setStyleSheet("color:white;")
        self.labelTitulo.setObjectName("labelTitulo")
        self.labelTitulo.setText('Título')
        self.verticalLayout_6.addWidget(self.labelTitulo)
        self.labelArtistas = QtWidgets.QLabel(self.frame_4)
        self.labelArtistas.setStyleSheet("color:grey;")
        self.labelArtistas.setText("artista")
        self.labelArtistas.setObjectName("labelArtistas")
        self.verticalLayout_6.addWidget(self.labelArtistas)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.horizontalLayout_2.addWidget(self.frame_4)
        self.frame_3 = QtWidgets.QFrame(self.reproduciendoFrame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pause_play = QtWidgets.QPushButton(self.frame_3)
        self.pause_play.setStyleSheet("QPushButton{\n"
                                      "    background:none;\n"
                                      "}")
        self.pause_play.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/tocar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pause_play.setIcon(icon2)
        self.pause_play.setIconSize(QtCore.QSize(40, 40))
        self.pause_play.setObjectName("pause_play")
        self.pause_play.clicked.connect(self.handle_play_pause)
        self.verticalLayout_5.addWidget(self.pause_play)
        self.horizontalSlider = QtWidgets.QSlider(self.frame_3)
        self.horizontalSlider.setStyleSheet("\n"
                                            "")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setProperty("value", 0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.sliderMoved.connect(self.set_song_duration_by_slider_position)
        self.horizontalSlider.sliderPressed.connect(self.player.pausar_cancion)
        self.horizontalSlider.sliderReleased.connect(self.player.reproductor.play)
        self.verticalLayout_5.addWidget(self.horizontalSlider)
        self.horizontalLayout_2.addWidget(self.frame_3)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 6)
        self.verticalLayout_2.addWidget(self.reproduciendoFrame)
        self.verticalLayout.addWidget(self.container)
        self.player.reproductor.positionChanged.connect(self.update_slider)
        self.player.reproductor.mediaChanged.connect(self._song_changed)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        for element in self.player.get_playlists():
            self.add_list(element)

        self.most_listened_action()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BlueBird"))
        self.mostListenedBtn.setText(_translate("MainWindow", "Mas Escuchadas"))
        self.favoritasBtn.setText(_translate("MainWindow", "Canciones Favoritas"))
        self.searchText.setPlaceholderText(_translate("MainWindow", "Buscar..."))
        self.listsLabel.setText(_translate("MainWindow", "Listas de Reproducción"))

    def add_song_to_frame(self, name, data=None):
        item = QListWidgetItem(name)
        item.setData(Qt.UserRole, data)

        self.songsList.addItem(item)

    def show_song_context_menu(self, pos):
        # Obtener el elemento seleccionado
        item = self.songsList.itemAt(pos)
        # Si no hay elementos seleccionados, salir
        if item is None:
            return

        # Crear una instancia de QMenu para nuestro menú contextual
        menu = QMenu(self.songsList)

        menu.setStyleSheet('QMenu {'
                           'border: 1px solid #d4d4d4;'
                           'padding: 4px;'
                           '}'
                           'QMenu::item {'
                           'padding: 2px 20px 2px 20px;'
                           'background-color: transparent;'
                           '}'
                           'QMenu::item:selected {'
                           'background-color: #0078d7;'
                           'color: #ffffff;'
                           '}'
                           'QMenu::separator {'
                           'height: 1px;'
                           'background-color: #d4d4d4;'
                           'margin: 4px 0px 4px 0px;'
                           '}'
                           )

        # Añadir acciones al menú contextual
        descargar = QAction('Descargar', menu)
        descargar.triggered.connect(partial(self.player.descargar_cancion, item.data(Qt.UserRole).split('||')[0], item.text()))
        menu.addAction(descargar)

        if not self.showing_favourites:
            añadir_favoritas = QAction('Añadir a favoritas', menu)
            añadir_favoritas.triggered.connect(partial(self.player.guardar_favoritas, item.data(Qt.UserRole)))
            menu.addAction(añadir_favoritas)
        submenu = QMenu("Añadir a Lista de reproduccion", menu)
        for element in self.player.get_playlists():
            pl = QAction(element, submenu)
            pl.triggered.connect(partial(self.player.añadir_cancion, element, item.data(Qt.UserRole)))
            submenu.addAction(pl)
        if self.is_playlist_showing:
            delete_from_playlist = QAction('Eliminar de la playlist', menu)
            delete_from_playlist.triggered.connect(
                partial(self.player.borrar_cancion, self.playlist_name, item.data(Qt.UserRole)))
            delete_from_playlist.triggered.connect(partial(self.songsList.takeItem, self.songsList.row(item)))
            menu.addAction(delete_from_playlist)

        if self.showing_favourites:
            delete_from_favourites = QAction('Eliminar de favoritas', menu)
            delete_from_favourites.triggered.connect(partial(self.player.eliminar_favoritas, item.data(Qt.UserRole)))
            delete_from_favourites.triggered.connect(partial(self.songsList.takeItem, self.songsList.row(item)))
            menu.addAction(delete_from_favourites)

        submenu.addSeparator()
        new = QAction('Nueva Lista +', submenu)


        new.triggered.connect(partial(self.new_list, item.data(Qt.UserRole)))
        submenu.addAction(new)
        menu.addMenu(submenu)
        # Mostrar el menú contextual en la posición del cursor

        action = menu.exec_(self.songsList.mapToGlobal(pos))

        # Ejecutar la acción correspondiente al hacer clic en el menú contextual
        if action is not None:
            if action.text() == "Eliminar":
                self.songsList.takeItem(self.songsList.row(item))

    def show_playlist_context_menu(self, object, name,  pos):

        # Crear una instancia de QMenu para nuestro menú contextual
        menu = QMenu()

        menu.setStyleSheet('QMenu {'
                           'border: 1px solid #d4d4d4;'
                           'padding: 4px;'
                           'background-color:#2F2C2C;'
                           '}'
                           'QMenu::item {'
                           'padding: 2px 20px 2px 20px;'
                           'background-color: transparent;'
                           'color:white;'
                           '}'
                           'QMenu::item:selected {'
                           'background-color: #0078d7;'
                           'color: #ffffff;'
                           '}'
                           'QMenu::separator {'
                           'height: 1px;'
                           'background-color: #d4d4d4;'
                           'margin: 4px 0px 4px 0px;'
                           '}'
                           )

        # Añadir acciones al menú contextual
        eliminar = QAction('Eliminar playlist', menu)
        eliminar.triggered.connect(partial(self.player.borrar_playlist, name))
        eliminar.triggered.connect(object.hide)
        eliminar.triggered.connect(self.songsList.clear)
        menu.addAction(eliminar)


        # Mostrar el menú contextual en la posición del cursor
        menu.exec_(object.mapToGlobal(pos))



    def song_selected(self):
        item = self.songsList.currentItem()
        url = item.data(Qt.UserRole).split('||')[0]
        self.player.current_title = item.data(Qt.UserRole).split('||')[1]
        self.player.current_artist = item.data(Qt.UserRole).split('||')[2]
        self.player.reproducir_cancion(url=url)

    def _song_changed(self, media):
        self.labelTitulo.setText(self.player.current_title)
        self.labelArtistas.setText(self.player.current_artist)

    def most_listened_action(self):

        self.songsList.clear()
        for cancion in self.player.obtener_canciones():
            self.add_song_to_frame(cancion['title_short'] + ' (' + cancion['artist']['name'] + ')',
                                   cancion['preview'] + '||' + cancion['title_short'] + '||' + cancion['artist'][
                                       'name'])
        self.is_playlist_showing = False
        self.showing_favourites = False

    def favourites_action(self):
        self.songsList.clear()
        for data in self.player.obtener_favoritas():
            self.add_song_to_frame(data.split('||')[1] + ' (' + data.split('||')[2] + ')', data)
        self.is_playlist_showing = False
        self.showing_favourites = True

    def search_songs(self):
        self.songsList.clear()
        for cancion in self.player.obtener_canciones_por_nombre(self.searchText.text()):
            self.add_song_to_frame(cancion['title_short'] + ' (' + cancion['artist']['name'] + ')',
                                   cancion['preview'] + '||' + cancion['title_short'] + '||' + cancion['artist'][
                                       'name'])
        self.is_playlist_showing = False
        self.showing_favourites = False

    def set_song_duration_by_slider_position(self, posicion):

        # Convertir la posición del control deslizante a milisegundos
        nueva_posicion = round(posicion * self.player.reproductor.duration() / 100)

        # Actualizar la posición del reproductor
        if (self.player.reproductor.duration() != 0):
            self.player.reproductor.setPosition(nueva_posicion)

    def update_slider(self, position):
        # Obtener la duración del archivo multimedia
        duracion = self.player.reproductor.duration()
        if ((position != 0) and (duracion != 0)):
            self.horizontalSlider.setValue(round(position * 100 / duracion))

    def handle_play_pause(self):
        if self.player.reproductor.state() == QMediaPlayer.State.PlayingState:
            self.player.pausar_cancion()
        else:
            self.player.reproductor.play()

