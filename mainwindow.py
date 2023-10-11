from typing import Optional, Tuple
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QSizePolicy,\
    QMainWindow, QPlainTextEdit, QWidget, QPushButton,\
    QSpinBox, QHBoxLayout, QVBoxLayout, QLabel, QApplication
from color_button import ColorButton
from qr_deploy import QrDeployWidget
from segno_using import Segno
from segno_uidata import AllSegnoData, MicroSegnoData, PdfSegnoData
from export_window import ExportWindow
from os import path
class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.data = Segno.encode("")
        self.setGeometry(20, 20, 500, 500)
        self.qr = QrDeployWidget(self)
        self.qr.setGeometry(0, 0, 500, 500)
        self.qr.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.MinimumExpanding)
        self.qr.setMinimumSize(100, 100)
        self.export_widget = ExportWindow()
        self.export_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        self.text = QPlainTextEdit(self)
        self.text.setGeometry(0, 0, 300, 50)
        self.text.setFixedHeight(100)
        
        self.fore_button = ColorButton()
        self.back_button = ColorButton()
        self.back_finder_button = ColorButton()
        self.fore_finder_button = ColorButton()
        self.border_button = ColorButton()
        
        self.scale_spin = QSpinBox()
        self.border_width_spin = QSpinBox()
        self.isMicro_button = QPushButton("Мікро")
        self.isMicro_button.setCheckable(True)
        self.connect_signals()
        self.load_default()
        self.place_ui()
        self.show()
    
    @property
    def color_buttons(self)-> Tuple[ColorButton]:
        return self.fore_button, self.back_button,\
                self.fore_finder_button, self.back_finder_button, self.border_button
    
    
    def load_default(self):
        self.back_button.current_color = QColor.fromRgb(255,255,255)
        self.border_button.current_color = QColor.fromRgb(255,255,255)
        self.back_finder_button.current_color = self.back_button.current_color
        self.scale_spin.setValue(10)
        self.border_width_spin.setValue(0)
        self.update_image()
        
    def bottom_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.qr, 1)
        layout.addWidget(self.export_widget, 1)
        return layout
     
    def top_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.text)
        
        colors = self.colors_layout()
        additional = self.additional_layout()
        settings = QVBoxLayout()
        settings.addLayout(colors)
        settings.addLayout(additional)
        layout.addLayout(settings)
        return layout
    
    def colors_layout(self):
        color_button_labels = "Перед", "Тло", "Перед кутів", "Тло кутів", "Границя"
        layout = QHBoxLayout()
        for i in range(len(self.color_buttons)):
            item_layout = QVBoxLayout()
            l =QLabel(color_button_labels[i])
            l.setWordWrap(True)
            self.color_buttons[i].setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Fixed)
            item_layout.addWidget(l)
            item_layout.addWidget(self.color_buttons[i])
            layout.addLayout(item_layout, 1)
        return layout
    
    def additional_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Множник"))
        layout.addWidget(self.scale_spin)
        layout.addWidget(QLabel("Границя"))
        layout.addWidget(self.border_width_spin)
        layout.addWidget(self.isMicro_button)
        return layout
    
    def place_ui(self):
        main_layout = QVBoxLayout()
        top = self.top_layout()
        bot = self.bottom_layout()
        main_layout.addLayout(top,1)
        main_layout.addLayout(bot)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def update_text(self):
        text = self.text.toPlainText()
        if self.isMicro_button.isChecked():
            self.data = Segno.encode_micro(text)
        else:
            self.data = Segno.encode(text)
        self.update_image()
    
    def connect_signals(self):
        for button in self.color_buttons:
            button.color_dialog.colorSelected.connect(self.update_image)
        self.text.textChanged.connect(self.update_text)
        self.export_widget.copy_button.clicked.connect(self.copy_image)
        self.export_widget.start_button.clicked.connect(self.export)   
        self.border_width_spin.valueChanged.connect(self.update_image)
        self.scale_spin.valueChanged.connect(self.update_image)
        self.isMicro_button.clicked.connect(self.update_text)
    
    
    def update_image(self):
        ui_data = self.collect_all_data()
        data = Segno.save_to_bytes(self.data, ui_data, "png")
        self.qr.update_pixmap(data)

    def copy_image(self):
        QApplication.clipboard().setPixmap(self.qr.label.pixmap())
    
    
    def collect_pdf_data(self) -> PdfSegnoData:
        ui_data = PdfSegnoData()
        ui_data.fore_color = self.fore_button.current_color.toTuple()
        ui_data.back_color = self.back_button.current_color.toTuple()
        ui_data.border_width = self.border_width_spin.value()
        ui_data.scale = self.scale_spin.value()
        return ui_data
    
    def collect_to_data(self, data: MicroSegnoData):
        data.fore_color = self.fore_button.current_color.toTuple()
        data.back_color = self.back_button.current_color.toTuple()
        data.finder_back_color = self.back_finder_button.current_color.toTuple()
        data.finder_fore_color = self.fore_finder_button.current_color.toTuple()
        data.border_width = self.border_width_spin.value()
        if data.border_width == 0:
            data.border_color = None
        else:    
            data.border_color = self.border_button.current_color.toTuple()
        data.scale = self.scale_spin.value()
    
    def collect_all_data(self) -> AllSegnoData:
        ui_data = AllSegnoData()
        self.collect_to_data(ui_data)
        return ui_data
    
    def collect_micro_data(self) -> MicroSegnoData:
        ui_data = MicroSegnoData()
        self.collect_to_data(ui_data)
        return ui_data
    
    def export(self):
        ext = self.export_widget.extension
        if ext == "pdf":
            data = self.collect_pdf_data()
        elif self.isMicro_button.isChecked():
            data = self.collect_micro_data()
        else:
            data = self.collect_all_data()
        file_path = path.join(self.export_widget.folder, self.export_widget.file_name+"."+ext)
        Segno.save_to_file(self.data, data, file_path, ext)