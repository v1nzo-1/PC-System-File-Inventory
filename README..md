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