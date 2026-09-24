# PC System & File Inventory

A Python-based system inventory tool that collects computer specifications, storage information, and file metadata.

## Features

- Computer name
- Manufacturer and model
- Operating system and Windows version
- System architecture
- CPU information
- Physical and logical CPU cores
- CPU speed and usage
- RAM information and usage
- GPU information
- Physical disk type
- Storage information
- Drive and file-system details
- File names and paths
- File extensions
- File sizes
- File-type statistics
- JSON and CSV report generation

## File Inventory

The program allows the user to select a folder and analyze its files.

It collects only file metadata:

- File name
- Relative path
- File extension
- File size in bytes
- File size in MB
- Total number of files
- Total storage used by files

## Reports

The program generates:

- `system_inventory_report.json`
- `file_inventory.csv`

All reports are generated locally on the computer.

## Privacy and Safety

This project performs local, read-only inventory.

It does not:

- Read file contents
- Execute files
- Delete files
- Modify files
- Upload information
- Collect passwords
- Collect browser cookies
- Install malicious software

Only scan computers and folders that you own or have permission to analyze.

Generated reports may contain computer information and should not be uploaded to a public repository.

## Technologies Used

- Python
- psutil
- PowerShell
- Windows CIM
- JSON
- CSV
- VS Code

## Project Structure

```text
pc_system_inventory/
│
├── system_info.py
├── README.md
├── requirements.txt
└── .gitignore
EX
=================================================================
             PC SYSTEM & FILE INVENTORY
=================================================================

[ COMPUTER ]
-----------------------------------------------------------------
Computer Name : MY-PC
Model         : Computer Model
Architecture  : AMD64

[ WINDOWS ]
-----------------------------------------------------------------
Operating System : Microsoft Windows
Windows Version  : Version
Windows Release  : Release

[ CPU ]
-----------------------------------------------------------------
Processor      : Processor Information
Physical Cores : 6
Logical Cores  : 12
Current Speed  : 4.20 GHz
Maximum Speed  : 4.50 GHz
CPU Usage      : 12.0 %

[ RAM ]
-----------------------------------------------------------------
Total RAM      : 16.0 GB
Used RAM       : 7.2 GB
Available RAM  : 8.8 GB
RAM Usage      : 45.0 %

[ STORAGE ]
-----------------------------------------------------------------
Drive          : C:\
File System    : NTFS
Total Space    : 476.94 GB
Used Space     : 210.52 GB
Free Space     : 266.42 GB
Storage Usage  : 44.1 %
