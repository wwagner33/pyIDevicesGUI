# pyIDevices GUI - Interface gráfica para dispositivos iOS no Linux
# Baseado no projeto original de Helltar (https://github.com/Helltar/idevicegui)
# Copyright (C) 2025 Wellington Wagner Ferreira Sarmento
#
# Este programa é software livre: você pode redistribuí-lo e/ou modificá-lo
# sob os termos da Licença Pública Geral GNU, conforme publicada pela Free Software Foundation,
# na versão 3 da Licença.
#
# Este programa é distribuído na esperança de que seja útil,
# mas SEM NENHUMA GARANTIA; sem mesmo a garantia implícita de
# COMERCIALIZAÇÃO ou ADEQUAÇÃO A UM DETERMINADO PROPÓSITO.
# Veja a Licença Pública Geral GNU para mais detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa. Se não, veja <https://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-

import subprocess
import re
from app import logger

# Constantes equivalentes às usadas no código Pascal
TOTAL_DATA_AVAILABLE = 'TotalDataAvailable'
TOTAL_DATA_CAPACITY = 'TotalDataCapacity'
TOTAL_DISK_CAPACITY = 'TotalDiskCapacity'


def run_command(*args):
    """Executa um comando subprocesso e retorna (stdout, exit_code)."""
    logger.debug(f"Executando comando: {' '.join(args)}")
    try:
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        logger.debug(f"Saída: {result.stdout.strip()}")
        return result.stdout.strip(), result.returncode
    except Exception as e:
        logger.error(f"Erro ao executar comando {args}: {e}")
        return str(e), -1



def get_disk_usage(dtype):
    """Retorna o valor int64 de uso de disco para um tipo especificado."""
    output, _ = run_command("ideviceinfo", "-q", "com.apple.disk_usage.factory", "-k", dtype)
    try:
        return int(output)
    except ValueError:
        return 0


def is_device_plugged():
    """Verifica se há um dispositivo conectado."""
    _, code = run_command("idevicename")
    return code == 0


def get_device_name():
    """Retorna o nome do dispositivo conectado."""
    output, _ = run_command("idevicename")
    return output


def get_device_info_by_key(key):
    """Obtém uma informação do dispositivo por chave (key)."""
    output, _ = run_command("ideviceinfo", "-k", key)
    return output.strip()


def get_device_cycle_count():
    """Extrai o valor de CycleCount de um dump XML do idevicediagnostics."""
    output, _ = run_command("idevicediagnostics", "diagnostics", "GasGauge")
    match = re.search(r"<key>CycleCount</key>.*?<integer>(\d+)</integer>", output, re.DOTALL)
    if match:
        return match.group(1)
    return "-1"
