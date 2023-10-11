import io
import segno
from segno_uidata import AllSegnoData, PdfSegnoData
class Segno:
    @staticmethod
    def encode(data: str) -> segno.QRCode:
        return segno.make_qr(data)
    
    @staticmethod
    def encode_micro(data: str) -> segno.QRCode:
        return segno.make_micro(data)
    
    
    @staticmethod
    def save_to_bytes(data: segno.QRCode, save_data: AllSegnoData, kind: str) -> io.BytesIO:
        buff = io.BytesIO()        
        data.save(buff, kind, **save_data)
        return buff
    
    
    @staticmethod
    def save_to_file(data: segno.QRCode, save_data: PdfSegnoData, file_name:str, kind:str)->None:
        data.save(file_name, kind, **save_data)
    