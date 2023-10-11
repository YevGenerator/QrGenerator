from typing import Optional
from PySide6.QtCore import Qt, QDir
from PySide6.QtWidgets import QLineEdit, QPushButton, QButtonGroup, QWidget, \
    QHBoxLayout, QVBoxLayout, QSizePolicy, QFileDialog
from segno_using import Segno

class ExportWindow(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.folder_text = QLineEdit()
        self.file_name_text = QLineEdit()
        self.start_button = QPushButton("Експортувати")
        self.copy_button = QPushButton("Копіювати")
        self.choices = QButtonGroup(self)
        self.browse_button = QPushButton("Знайти...")
        self.build_layout()
        self.connect_signals()
        self.show()
        
        self._folder_exists =False
        self._file_is_filled = False
        self.update_enabled_start()
    
    @property
    def file_name(self):
        return self.file_name_text.text()
    
    @property
    def folder(self):
        return self.folder_text.text()

    @property
    def extension(self):
        return self.choices.checkedButton().text().lower()
    
    def connect_signals(self):
        self.browse_button.clicked.connect(self.update_folder_path)
        self.folder_text.textChanged.connect(self.enable_export_by_folder)
        self.file_name_text.textChanged.connect(self.enable_export_by_file)
        
    def enable_export_by_folder(self):
        self._folder_exists = QDir(self.folder).exists()
        self.update_enabled_start()
        
    def enable_export_by_file(self):
        self._file_is_filled = self.file_name != ""
        self.update_enabled_start()
        
    def update_enabled_start(self):
        self.start_button.setEnabled(self._folder_exists and self._file_is_filled)

    
    def update_folder_path(self):
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)
        folder_dialog.setOption(QFileDialog.Option.ShowDirsOnly)
        if folder_dialog.exec():
            self.folder_text.setText(folder_dialog.selectedFiles()[0])
        
    def build_layout(self):
        main_layout = QVBoxLayout()
        choice_layout = QHBoxLayout()
        file_layout = QVBoxLayout()
        folder_layout  = QHBoxLayout()
        start_layout = QHBoxLayout()
        folder_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        file_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        choice_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        start_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.file_name_text.setPlaceholderText("Назва файлу без розширення")
        self.folder_text.setPlaceholderText("Тека збереження")
        self.folder_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.browse_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        folder_layout.addWidget(self.folder_text)
        folder_layout.addWidget(self.browse_button)
        names = "PDF", "SVG", "PNG"
        for name in names:
            button = QPushButton(name)
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
            self.choices.addButton(button) 
            choice_layout.addWidget(button)
        self.choices.buttons()[0].setChecked(True)
        file_layout.addWidget(self.file_name_text)
        file_layout.addLayout(choice_layout)
        
        start_layout.addWidget(self.copy_button)
        start_layout.addWidget(self.start_button)
        
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addLayout(folder_layout)
        main_layout.addLayout(file_layout)
        main_layout.addLayout(start_layout)
        self.setLayout(main_layout)
    
    