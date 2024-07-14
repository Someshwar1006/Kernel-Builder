# main.py

import os
import requests
import subprocess
import argparse
from bs4 import BeautifulSoup

KERNEL_BASE_URL = "https://www.kernel.org"

def get_available_versions(debug=False):
    url = f"{KERNEL_BASE_URL}/releases.json"
    if debug:
        print(f"Fetching available versions from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        versions = response.json().get('releases')
        if debug:
            print(f"Fetched {len(versions)} versions")
        return versions
    else:
        print("Failed to fetch kernel versions. Check your internet connection.")
        return []

def format_version_info(version_info):
    version = version_info.get('version', 'Unknown Version')
    released_date = version_info.get('released', {}).get('isodate', 'Unknown Date')
    source_url = version_info.get('source', 'Unknown Source')
    return f"{version} - Released: {released_date}\n   Source: {source_url}"

def choose_kernel_version(versions, debug=False):
    print("Available Linux Kernel Versions:")
    for idx, version_info in enumerate(versions, start=1):
        formatted_info = format_version_info(version_info)
        print(f"{idx}. {formatted_info}")

    while True:
        try:
            selection = input("Enter the number of the kernel version to build: ")
            index = int(selection) - 1
            if 0 <= index < len(versions):
                if debug:
                    print(f"Selected version: {versions[index].get('version')}")
                return versions[index].get('version')
            else:
                print("Invalid selection. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def download_kernel(version, debug=False):
    url = f"{KERNEL_BASE_URL}/pub/linux/kernel/v{version.split('.')[0]}.x/linux-{version}.tar.xz"
    if debug:
        print(f"Downloading kernel from {url}")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(f"linux-{version}.tar.xz", 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded linux-{version}.tar.xz")
        if debug:
            print(f"Kernel downloaded to linux-{version}.tar.xz")
    else:
        print("Failed to download kernel. Check the version and try again.")

def extract_kernel(version, debug=False):
    if debug:
        print(f"Extracting linux-{version}.tar.xz")
    os.system(f"tar -xf linux-{version}.tar.xz")
    print(f"Extracted linux-{version}")
    if debug:
        print(f"Kernel extracted to linux-{version}")

def configure_kernel(version, debug=False):
    os.chdir(f"linux-{version}")
    print("Configuration options:")
    print("1. Use default configuration")
    print("2. Choose configuration from scratch")
    print("3. Customize from default configuration")
    while True:
        config_option = input("Enter your choice (1/2/3): ")
        if config_option == '1':
            if debug:
                print("Running 'make defconfig'")
            os.system("make defconfig")
            print("Kernel configured with default options")
            break
        elif config_option == '2':
            if debug:
                print("Running 'make menuconfig'")
            os.system("make menuconfig")
            print("Kernel configuration completed from scratch")
            break
        elif config_option == '3':
            if debug:
                print("Running 'make defconfig' followed by 'make menuconfig'")
            os.system("make defconfig")
            os.system("make menuconfig")
            print("Kernel configuration customized from default options")
            break
        else:
            print("Invalid selection. Please enter 1, 2, or 3.")

def compile_kernel(version, debug=False):
    if debug:
        print("Running 'make -j$(nproc)'")
    os.system("make -j$(nproc)")
    print("Kernel compilation complete")

def install_kernel(version, debug=False):
    if debug:
        print("Running 'sudo make modules_install'")
    os.system("sudo make modules_install")
    os.system(f"sudo cp -v arch/x86/boot/bzImage /boot/vmlinuz-{version}")
    os.system(f"sudo cp -v System.map /boot/System.map-{version}")
    os.system(f"sudo cp -v .config /boot/config-{version}")
    print("Kernel installed")

def create_initramfs(version, debug=False):
    initramfs_path = f"/boot/initramfs-{version}.img"
    if debug:
        print(f"Creating initramfs at {initramfs_path}")
    os.system(f"sudo mkinitcpio -k {version} -g {initramfs_path}")
    print(f"Initramfs created at {initramfs_path}")

def update_bootloader(version, debug=False):
    if debug:
        print("Updating bootloader")
    os.system("sudo update-grub")
    print("Bootloader updated")

def main():
    parser = argparse.ArgumentParser(description="Linux Kernel Builder")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    debug = args.debug

    available_versions = get_available_versions(debug)
    if not available_versions:
        return

    selected_version = choose_kernel_version(available_versions, debug)

    download_kernel(selected_version, debug)
    extract_kernel(selected_version, debug)
    configure_kernel(selected_version, debug)
    compile_kernel(selected_version, debug)
    install_kernel(selected_version, debug)
    create_initramfs(selected_version, debug)
    update_bootloader(selected_version, debug)

if __name__ == "__main__":
    main()
