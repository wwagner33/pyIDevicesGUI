import shutil

REQUIRED_COMMANDS = [
    "ideviceinfo",
    "idevicename",
    "idevicediagnostics",
    "ideviceimagemounter",
    "idevicebackup2",
    "usbmuxd",
]

def check_dependencies():
    """Verifica se todos os comandos necessários estão disponíveis no sistema."""

    missing = [cmd for cmd in REQUIRED_COMMANDS if shutil.which(cmd) is None]

    if missing:
        print("\n❌ As seguintes dependências estão ausentes:")
        for cmd in missing:
            print(f"  - {cmd}")
        print("\nPara instalá-las no Fedora, execute:")
        print("  sudo dnf install libimobiledevice usbmuxd\n")
        return False

    print("✅ Todas as dependências do libimobiledevice estão corretamente instaladas.")
    return True
