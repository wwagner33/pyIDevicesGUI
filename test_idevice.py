#!/usr/bin/env python3

from app import idevice


def main():
    print("🔌 Verificando conexão com dispositivo iOS...")

    if not idevice.is_device_plugged():
        print("❌ Nenhum dispositivo iOS conectado.")
        return

    print("✅ Dispositivo conectado!")

    name = idevice.get_device_name()
    print(f"📱 Nome do dispositivo: {name}")

    cycle_count = idevice.get_device_cycle_count()
    print(f"🔋 Ciclos de bateria: {cycle_count}")

    total_disk = idevice.get_disk_usage(idevice.TOTAL_DISK_CAPACITY)
    used_disk = idevice.get_disk_usage(idevice.TOTAL_DATA_CAPACITY)
    available_disk = idevice.get_disk_usage(idevice.TOTAL_DATA_AVAILABLE)

    print(f"💾 Armazenamento total: {total_disk // (1024**3)} GB")
    print(f"💾 Espaço usado: {used_disk // (1024**3)} GB")
    print(f"💾 Espaço livre: {available_disk // (1024**3)} GB")

    ios_version = idevice.get_device_info_by_key("ProductVersion")
    print(f"📱 iOS: {ios_version}")

if __name__ == "__main__":
    main()
