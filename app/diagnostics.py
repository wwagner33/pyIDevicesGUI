import subprocess
from app import logger

def obter_diagnostico():
    try:
        logger.info("Executando idevicediagnostics diagnostics")
        result = subprocess.run(
            ["idevicediagnostics", "diagnostics", "GasGauge"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        logger.exception("Erro ao executar diagnóstico")
        return False, str(e)
