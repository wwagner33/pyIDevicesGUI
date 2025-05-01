import subprocess
import os
from datetime import datetime
from app import logger

def capturar_screenshot(destino_pasta):
    nome_arquivo = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    caminho = os.path.join(destino_pasta, nome_arquivo)

    try:
        logger.info(f"Capturando screenshot: {caminho}")
        result = subprocess.run(
            ["idevicescreenshot", caminho],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True, caminho
        else:
            return False, result.stderr
    except Exception as e:
        logger.exception("Erro ao capturar screenshot")
        return False, str(e)
