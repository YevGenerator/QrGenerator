from typing import Optional
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtWidgets import QWidget, QLabel
import io

class QrDeployWidget(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        
        self.label = QLabel(self)
        self.show()
    
    def update_pixmap(self, bytes: io.BytesIO):
        pixmap = QPixmap()
        pixmap.loadFromData(bytes.getvalue())
        min_size = self.get_min_size()
        pixmap = pixmap.scaled(min_size, min_size)
        self.label.setFixedSize(min_size, min_size)
        self.label.setPixmap(pixmap)
    
    def get_min_size(self):
        width = self.width()
        height = self.height()
        min_size = height if height < width else width
        return min_size
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        min_size = self.get_min_size()
        self.label.setFixedSize(min_size, min_size)
        pic = self.label.pixmap()
        if not pic.isNull():
            self.label.setPixmap(pic.scaled(min_size, min_size))
        