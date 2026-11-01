#TODO Save the interface location between runs
import sys

from PyQt6.QtCore import Qt,pyqtSignal,QTimer,QCoreApplication
from PyQt6.QtWidgets import QApplication,QGridLayout,QWidget,QLabel
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
        self.elements = []
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

        self.light_dungeon_icon = QLabel("")
        self.light_dungeon_icon.setPixmap(QPixmap(str(HOME / "sfhelpers" / "resources" / "dungeon_icon.png")).scaled(36,36))

        self.city_guard_icon = QLabel("")
        self.city_guard_icon.setPixmap(QPixmap(str(HOME / "sfhelpers" / "resources" / "city_guard_icon.png")).scaled(36,36))

        self.gem_mine_icon = QLabel("")
        self.gem_mine_icon.setPixmap(QPixmap(str(HOME / "sfhelpers" / "resources" / "gem_mine_icon.png")).scaled(36,36))

        self.arena_label = QLabel("")
        self.light_dungeon_label = QLabel("")
        self.city_guard_label = QLabel("")
        self.gem_mine_label = QLabel("")
        self.character_name_label = QLabel("")

        self.arena_label.setObjectName("arena_label")
        self.arena_icon.setObjectName("arena_icon")
        self.elements.append(self.arena_label)
        self.elements.append(self.arena_icon)

        self.light_dungeon_label.setObjectName("light_dungeon_label")
        self.light_dungeon_icon.setObjectName("light_dungeon_icon")
        self.elements.append(self.light_dungeon_label)
        self.elements.append(self.light_dungeon_icon)

        self.city_guard_label.setObjectName("city_guard_label")
        self.city_guard_icon.setObjectName("city_guard_icon")
        self.elements.append(self.city_guard_label)
        self.elements.append(self.city_guard_icon)

        self.gem_mine_label.setObjectName("gem_mine_label")
        self.gem_mine_icon.setObjectName("gem_mine_icon")
        self.elements.append(self.gem_mine_label)
        self.elements.append(self.gem_mine_icon)
        self.main_layout.addWidget(self.character_name_label,0,0,1,0,Qt.AlignmentFlag.AlignCenter)
        
        self.create_main_layout()

        self.set_character_status()
        self.update_timers()
        self.update_timer.start(1000)
        self.character_name_label.setText(self.current_character["name"])

    def create_main_layout(self):
        config_layout = self.read_config()[1:]
        row = 0
        for line in config_layout:
            config = line.split(":")
            if(config[1].strip() == "1"):
                row += 1
                target_elements = [element for element in self.elements if element.objectName() == config[0] + "_label" or element.objectName() == config[0]  + "_icon"]
                
                for i,elemenet in enumerate(target_elements[::-1]):
                    self.main_layout.addWidget(elemenet,row,i)


        self.setLayout(self.main_layout)
        
    def read_config(self):
        try:
            with open(HOME / "config.txt","r") as f:
                return f.readlines()
        except FileNotFoundError:
            with open(HOME / "backup" / "config_backup.txt","r") as f:
                config = f.read()
            with open(HOME / "config.txt","w") as f:
                f.write(config)
            return self.read_config()


    def write_to_config(self,config):
        pass

    def set_character_status(self):
        self.status[self.current_character["name"]] = get_character_status(self.session,self.current_character)

    def update_timers(self):
        target_character = self.current_character
        current_status = self.status[self.current_character["name"]]

        self.arena_label.setText(calculate_remaining(target_character["timezone_diff"],current_status["arena"]))
        self.light_dungeon_label.setText(calculate_remaining(target_character["timezone_diff"],current_status["characterstatus"]["light_dungeon"]))
        self.city_guard_label.setText(calculate_remaining(target_character["timezone_diff"],current_status["characterstatus"]["city_guard"]))
        if(current_status.get("fortress","")):
            self.gem_mine_label.setText(calculate_remaining(target_character["timezone_diff"],current_status["fortress"]["gem_mine"]))
        else:
            self.gem_mine_label.setText("You don't have the fortress yet")
    
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
        if not self.is_cd:
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
