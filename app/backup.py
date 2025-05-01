import subprocess
import os
from app import logger

def realizar_backup(destino):
    """Executa backup usando idevicebackup2"""
    try:
        logger.info(f"Iniciando backup para: {destino}")
        os.makedirs(destino, exist_ok=True)
        result = subprocess.run(
            ["idevicebackup2", "backup", destino],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info("Backup concluído com sucesso.")
            return True, result.stdout
        else:
            logger.error(f"Erro ao realizar backup: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        logger.exception(f"Exceção durante o backup: {e}")
        return False, str(e)
