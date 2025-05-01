import subprocess
from app import logger

def listar_usb():
    """Retorna a lista dos dispositivos USB conectados (via lsusb)"""
    try:
        resultado = subprocess.run(["lsusb"], capture_output=True, text=True)
        logger.info("Listagem de dispositivos USB executada com sucesso.")
        return True, resultado.stdout
    except Exception as e:
        logger.exception("Erro ao executar lsusb")
        return False, str(e)

def listar_detalhes_usb():
    """Retorna saída do comando usb-devices (mais detalhada)"""
    try:
        resultado = subprocess.run(["usb-devices"], capture_output=True, text=True)
        return True, resultado.stdout
    except Exception as e:
        logger.exception("Erro ao executar usb-devices")
        return False, str(e)
