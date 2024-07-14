# main.py

import os
import requests
import subprocess
import argparse
from bs4 import BeautifulSoup

KERNEL_BASE_URL = "https://www.kernel.org"

def get_available_versions():
    url = f"{KERNEL_BASE_URL}/releases.json"
    response = requests.get(url)
    if response.status_code == 200:
        versions = response.json().get('releases')
        return versions
    else:
        print("Failed to fetch kernel versions. Check your internet connection.")
        return []

def format_version_info(version_info):
    version = version_info.get('version', 'Unknown Version')
    released_date = version_info.get('released', {}).get('isodate', 'Unknown Date')
    source_url = version_info.get('source', 'Unknown Source')
    return f"{version} - Released: {released_date}\n   Source: {source_url}"

def choose_kernel_version(versions):
    print("Available Linux Kernel Versions:")
    for idx, version_info in enumerate(versions, start=1):
        formatted_info = format_version_info(version_info)
        print(f"{idx}. {formatted_info}")

    while True:
        try:
            selection = input("Enter the number of the kernel version to build: ")
            index = int(selection) - 1
            if 0 <= index < len(versions):
                return versions[index].get('version')
            else:
                print("Invalid selection. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def download_kernel(version):
    url = f"{KERNEL_BASE_URL}/pub/linux/kernel/v{version.split('.')[0]}.x/linux-{version}.tar.xz"
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(f"linux-{version}.tar.xz", 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded linux-{version}.tar.xz")
    else:
        print("Failed to download kernel. Check the version and try again.")

def extract_kernel(version):
    os.system(f"tar -xf linux-{version}.tar.xz")
    print(f"Extracted linux-{version}")

def configure_kernel(version):
    os.chdir(f"linux-{version}")
    os.system("make defconfig")
    print("Kernel configured with default options")

def compile_kernel(version):
    os.system("make -j$(nproc)")
    print("Kernel compilation complete")

def install_kernel(version):
    os.system("sudo make modules_install")
    os.system(f"sudo cp -v arch/x86/boot/bzImage /boot/vmlinuz-{version}")
    os.system(f"sudo cp -v System.map /boot/System.map-{version}")
    os.system(f"sudo cp -v .config /boot/config-{version}")
    print("Kernel installed")

def update_bootloader(version):
    os.system("sudo update-grub")
    print("Bootloader updated")

def main():
    available_versions = get_available_versions()
    if not available_versions:
        return

    selected_version = choose_kernel_version(available_versions)

    download_kernel(selected_version)
    extract_kernel(selected_version)
    configure_kernel(selected_version)
    compile_kernel(selected_version)
    install_kernel(selected_version)
    update_bootloader(selected_version)

if __name__ == "__main__":
    main()
