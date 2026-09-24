import os
import platform
import socket
import shutil
import csv
import json
import subprocess
from pathlib import Path
from datetime import datetime

import psutil


def gb(value):
    return round(value / (1024 ** 3), 2)


def get_windows_info():
    try:
        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-CimInstance Win32_OperatingSystem).Caption"
            ],
            text=True
        ).strip()
        return result
    except Exception:
        return "Unknown"


def get_pc_model():
    try:
        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-CimInstance Win32_ComputerSystem).Manufacturer + ' ' + (Get-CimInstance Win32_ComputerSystem).Model"
            ],
            text=True
        ).strip()
        return result
    except Exception:
        return "Unknown"


def get_gpu():
    try:
        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-CimInstance Win32_VideoController).Name"
            ],
            text=True
        ).strip()

        return result.replace("\n", ", ")
    except Exception:
        return "Unknown"


def get_disk_type():
    try:
        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-PhysicalDisk | Select-Object -ExpandProperty MediaType)"
            ],
            text=True
        ).strip()

        return result.replace("\n", ", ")
    except Exception:
        return "Unknown"


def get_system_info():

    ram = psutil.virtual_memory()

    return {
        "computer_name": socket.gethostname(),
        "manufacturer_model": get_pc_model(),
        "operating_system": get_windows_info(),
        "windows_version": platform.version(),
        "windows_release": platform.release(),
        "architecture": platform.machine(),

        "processor": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),

        "ram_total_gb": gb(ram.total),
        "ram_used_gb": gb(ram.used),
        "ram_available_gb": gb(ram.available),
        "ram_usage_percent": ram.percent,

        "gpu": get_gpu(),
        "disk_type": get_disk_type(),

        "python_version": platform.python_version()
    }


def get_storage_info():

    drives = []

    for disk in psutil.disk_partitions():

        if "cdrom" in disk.opts.lower():
            continue

        try:
            usage = psutil.disk_usage(disk.mountpoint)

            drives.append({
                "drive": disk.device,
                "mount_point": disk.mountpoint,
                "file_system": disk.fstype,
                "total_gb": gb(usage.total),
                "used_gb": gb(usage.used),
                "free_gb": gb(usage.free),
                "usage_percent": usage.percent
            })

        except (PermissionError, OSError):
            pass

    return drives


def scan_folder(folder):

    files = []
    extension_summary = {}

    folder = Path(folder)

    for root, _, filenames in os.walk(folder):

        for filename in filenames:

            file_path = Path(root) / filename

            try:
                size = file_path.stat().st_size
            except (PermissionError, OSError):
                continue

            extension = file_path.suffix.lower()

            if not extension:
                extension = "[no extension]"

            relative_path = file_path.relative_to(folder)

            file_data = {
                "name": filename,
                "path": str(relative_path),
                "extension": extension,
                "size_bytes": size,
                "size_mb": round(size / (1024 ** 2), 2)
            }

            files.append(file_data)

            if extension not in extension_summary:

                extension_summary[extension] = {
                    "count": 0,
                    "size_bytes": 0
                }

            extension_summary[extension]["count"] += 1
            extension_summary[extension]["size_bytes"] += size

    return files, extension_summary


def save_json(system, storage, files, summary, folder):

    report = {
        "generated_at": datetime.now().isoformat(),
        "system_information": system,
        "storage_information": storage,
        "folder_analyzed": str(folder),
        "total_files": len(files),
        "file_type_summary": summary,
        "files": files
    }

    with open(
        "system_inventory_report.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(report, file, indent=4)


def save_csv(files):

    with open(
        "file_inventory.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "name",
                "path",
                "extension",
                "size_bytes",
                "size_mb"
            ]
        )

        writer.writeheader()
        writer.writerows(files)


def display_system_info(system):

    print("\n[ COMPUTER ]")
    print("-" * 65)

    print("Computer Name :", system["computer_name"])
    print("Model         :", system["manufacturer_model"])
    print("Architecture  :", system["architecture"])

    print("\n[ WINDOWS ]")
    print("-" * 65)

    print("Operating System :", system["operating_system"])
    print("Windows Version  :", system["windows_version"])
    print("Windows Release  :", system["windows_release"])

    print("\n[ CPU ]")
    print("-" * 65)

    print("Processor      :", system["processor"])
    print("Physical Cores :", system["physical_cores"])
    print("Logical Cores  :", system["logical_cores"])

    cpu = psutil.cpu_freq()

    if cpu:

        print(
            "Current Speed  :",
            round(cpu.current / 1000, 2),
            "GHz"
        )

        print(
            "Maximum Speed  :",
            round(cpu.max / 1000, 2),
            "GHz"
        )

    print(
        "CPU Usage      :",
        psutil.cpu_percent(interval=1),
        "%"
    )

    print("\n[ RAM ]")
    print("-" * 65)

    print(
        "Total RAM      :",
        system["ram_total_gb"],
        "GB"
    )

    print(
        "Used RAM       :",
        system["ram_used_gb"],
        "GB"
    )

    print(
        "Available RAM  :",
        system["ram_available_gb"],
        "GB"
    )

    print(
        "RAM Usage      :",
        system["ram_usage_percent"],
        "%"
    )

    print("\n[ GPU ]")
    print("-" * 65)

    print("Graphics Card  :", system["gpu"])

    print("\n[ PHYSICAL DISK ]")
    print("-" * 65)

    print("Disk Type      :", system["disk_type"])


def display_storage(storage):

    print("\n[ STORAGE ]")
    print("-" * 65)

    for drive in storage:

        print("\nDrive          :", drive["drive"])
        print("File System    :", drive["file_system"])
        print("Total Space    :", drive["total_gb"], "GB")
        print("Used Space     :", drive["used_gb"], "GB")
        print("Free Space     :", drive["free_gb"], "GB")
        print("Storage Usage  :", drive["usage_percent"], "%")


def display_file_summary(files, summary):

    total_size = sum(
        file["size_bytes"]
        for file in files
    )

    print("\n[ FILE INVENTORY ]")
    print("-" * 65)

    print("Total Files    :", len(files))
    print("Total Size     :", gb(total_size), "GB")

    print("\nFile Type Summary")
    print("-" * 65)

    print(
        f"{'Extension':20}"
        f"{'Count':10}"
        f"{'Size (MB)':15}"
    )

    print("-" * 65)

    for extension, data in sorted(
        summary.items(),
        key=lambda item: item[1]["size_bytes"],
        reverse=True
    ):

        print(
            f"{extension:20}"
            f"{data['count']:<10}"
            f"{data['size_bytes'] / (1024 ** 2):.2f}"
        )


def main():

    os.system("cls" if os.name == "nt" else "clear")

    print("=" * 65)
    print("             PC SYSTEM & FILE INVENTORY")
    print("=" * 65)

    print("\nThis program:")
    print("✓ Reads PC specifications")
    print("✓ Reads storage information")
    print("✓ Reads file names, extensions and sizes")
    print("✓ Creates local JSON and CSV reports")
    print()
    print("It does NOT:")
    print("✗ Open file contents")
    print("✗ Execute files")
    print("✗ Delete files")
    print("✗ Modify files")
    print("✗ Upload information")

    system = get_system_info()
    storage = get_storage_info()

    display_system_info(system)
    display_storage(storage)

    print("\n" + "=" * 65)

    folder = input(
        "\nEnter a folder to analyze "
        "(or press ENTER to skip): "
    ).strip().strip('"')

    files = []
    summary = {}

    if folder:

        folder_path = Path(folder).expanduser()

        if folder_path.exists() and folder_path.is_dir():

            print("\nScanning folder...")

            files, summary = scan_folder(folder_path)

            display_file_summary(files, summary)

            save_json(
                system,
                storage,
                files,
                summary,
                folder_path
            )

            save_csv(files)

            print("\nReports created:")
            print("✓ system_inventory_report.json")
            print("✓ file_inventory.csv")

        else:

            print("\nInvalid folder path.")
            print("System information was still collected.")

    else:

        save_json(
            system,
            storage,
            files,
            summary,
            "No folder selected"
        )

        print("\nSystem report created:")
        print("✓ system_inventory_report.json")

    print("\n" + "=" * 65)
    print("                 ANALYSIS COMPLETE")
    print("=" * 65)

    input("\nPress ENTER to close...")


if __name__ == "__main__":
    main()