from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget, QPushButton, QColorDialog

class ColorButton(QPushButton):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        self.color_dialog = QColorDialog()
        self.current_color = QColor.fromRgb(0,0,0)
        self.color_dialog.colorSelected.connect(self.on_color_selected)
        self.clicked.connect(self.color_dialog.open)
        self.setFlat(True)
        self.setFixedSize(60, 60)
    
    def on_color_selected(self, color: QColor):
        self.current_color = color
    
    @property
    def current_color(self) -> QColor:
        return self._current_color
    
    @current_color.setter
    def current_color(self, value: QColor):
        self._current_color = value
        self.update_back()
    
    def update_back(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Button, self.current_color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)



        