#TODO Save the interface location between runs
import sys

from PyQt6.QtCore import Qt,pyqtSignal,QTimer
from PyQt6.QtWidgets import QMainWindow, QApplication,QGridLayout,QWidget,QLabel
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QPixmap

from sfhelpers.sf_logining import get_session,fill_server_map
from sfhelpers.sf_main import get_characters,get_character_status,calculate_remaining
from credential_manager import load_credentials,obtain_credentials,save_credentials

from pathlib import Path
from itertools import cycle
from pynput import keyboard


HOME = Path(__file__).resolve().parent
credentials = {}

class MainWindow(QWidget):
    hotkey_press_signal = pyqtSignal()
    exit_press_signal = pyqtSignal()
    update_press_signal = pyqtSignal()
    change_press_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.dragging = False
        self.main_layout = QGridLayout(self)
        self.status = {}
        self.session = get_session(credentials)
        self.is_cd = False
        
        self.characters = get_characters(self.session)
        
        self.characters_indices = cycle(range(len(self.characters)))
        self.current_character = self.characters[next(self.characters_indices)]

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        #self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        #Keys signals connections
        self.hotkey_press_signal.connect(self.display_interface)
        self.exit_press_signal.connect(self.exit)
        self.update_press_signal.connect(self.update_character_status)
        self.change_press_signal.connect(self.change_current_character)


        self.hot_keys_listener = keyboard.GlobalHotKeys({"<alt>+s":self.emit_display_hot_key,
                                                         "<alt>+x":self.emit_exit_hot_key,
                                                         "<alt>+c":self.emit_change_hot_key,
                                                         "<alt>+u":self.emit_update_hot_key}
                                                        ,daemon=True)
        self.hot_keys_listener.start()
        
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_timers)
    
        self.arena_icon = QLabel("")
        self.arena_icon.setPixmap(QPixmap(str(HOME / "sfhelpers" / "resources" / "arena_icon.png")).scaled(36,36))

        self.dungeon_icon = QLabel("")
        self.dungeon_icon.setPixmap(QPixmap(str(HOME / "sfhelpers" / "resources" / "dungeon_icon.png")).scaled(36,36))
        
        self.arena_label = QLabel("")
        self.dungeon_label = QLabel("")
        self.character_name_label = QLabel("")

        self.main_layout.addWidget(self.character_name_label,0,0)

        self.main_layout.addWidget(self.arena_icon,1,0)
        self.main_layout.addWidget(self.arena_label,1,1)
        self.main_layout.addWidget(self.dungeon_icon,2,0)
        self.main_layout.addWidget(self.dungeon_label,2,1)


        self.setLayout(self.main_layout)

        self.set_character_status()
        self.update_timers()
        self.update_timer.start(1000)
        self.character_name_label.setText(self.current_character["name"])

    def set_character_status(self):
        self.status[self.current_character["name"]] = get_character_status(self.session,self.current_character)

    def update_timers(self):
        target_character = self.current_character
        self.arena_label.setText(calculate_remaining(target_character["timezone_diff"],self.status[self.current_character["name"]]["arena"]))
        self.dungeon_label.setText(calculate_remaining(target_character["timezone_diff"],self.status[self.current_character["name"]]["characterstatus"]))
    
    def disable_cd(self):
        self.is_cd = False


    #Mouse events used for dragging the interface
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = self.mapToParent(event.pos() - self.offset)
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    #Keyboard related events
    def display_interface(self):
        if(self.isHidden()):
            self.show()
        else:
            self.hide()
    
    def exit(self):
        self.hot_keys_listener.stop()
        QCoreApplication.exit()
    
    def update_character_status(self):
        if not self.is_cd:
            self.is_cd = True
            self.update_timer.stop()
            self.set_character_status()
            self.update_timers()
            self.update_timer.start(1000)
            QTimer().singleShot(5000,self.disable_cd)
        

    def change_current_character(self):
        self.update_timer.stop()
        self.current_character = self.characters[next(self.characters_indices)]
        if(not self.status.get(self.current_character["name"],None)):
            self.is_cd = True
            self.set_character_status()
            QTimer().singleShot(5000,self.disable_cd)
        
        self.update_timers()
        self.update_timer.start(1000)
        self.character_name_label.setText(self.current_character["name"])      

    #Keys emit
    def emit_display_hot_key(self):
        self.hotkey_press_signal.emit()

    def emit_exit_hot_key(self):
        self.exit_press_signal.emit()

    def emit_update_hot_key(self):
        self.update_press_signal.emit()

    def emit_change_hot_key(self):
        self.change_press_signal.emit()

if __name__ == '__main__':
    credentials = load_credentials()

    if(not credentials):
        credentials = obtain_credentials()  
        save_credentials(credentials)      
            
    fill_server_map()

    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    app.exec()
