from PyQt6.QtWidgets import (QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QLabel,QCheckBox
                            ,QListWidget,QListWidgetItem)
from PyQt6.QtCore import pyqtSignal

class Popup(QWidget):
    save_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.list_layout = QListWidget()
        self.list_layout.setDragDropMode(QListWidget.DragDropMode.InternalMove)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.list_layout)
        self.main_layout.addWidget(self.save_button)

    def add_row(self,text,checkbox_status):
        self.item = QListWidgetItem()
        self.list_layout.addItem(self.item)

        self.row_widget = QWidget()
        self.hbox_layout = QHBoxLayout(self.row_widget)

        self.hbox_layout.addWidget(QLabel(text))
        
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(checkbox_status)
           
        self.hbox_layout.addWidget(self.checkbox)
        self.item.setSizeHint(self.row_widget.sizeHint())
        self.list_layout.setItemWidget(self.item,self.row_widget)
    

    def read_rows_config(self,configs):
        for config in configs[1:]:
            splitted_config = config.split(":")

            self.add_row(splitted_config[0],int(splitted_config[1]))
    
    def save_config(self):
        config_list = []
        for i in range(self.list_layout.count()):
            item = self.list_layout.item(i)
            widget = self.list_layout.itemWidget(item)

            label_text = widget.findChild(QLabel).text()
            checkbox_status = str(int(widget.findChild(QCheckBox).isChecked()))
            config_list.append((label_text,checkbox_status))
        self.save_signal.emit(config_list)
