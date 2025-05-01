import subprocess
from app import logger

def montar_imagem(dmg_path):
    try:
        logger.info(f"Montando imagem: {dmg_path}")
        result = subprocess.run(
            ["ideviceimagemounter", dmg_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        logger.exception("Erro ao montar imagem")
        return False, str(e)
