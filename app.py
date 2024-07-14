import os
import requests
import subprocess
import argparse
import tarfile

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
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        with open(f"linux-{version}.tar.xz", 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    print_progress_bar(downloaded_size, total_size, prefix="Downloading:", suffix="Complete", length=50)
        print(f"\nDownloaded linux-{version}.tar.xz")
        if debug:
            print(f"Kernel downloaded to linux-{version}.tar.xz")
    else:
        print("Failed to download kernel. Check the version and try again.")

def extract_kernel(version, debug=False):
    if debug:
        print(f"Extracting linux-{version}.tar.xz")
    with tarfile.open(f"linux-{version}.tar.xz", 'r:xz') as tar:
        total_files = len(tar.getmembers())
        extracted_files = 0
        for member in tar.getmembers():
            tar.extract(member)
            extracted_files += 1
            print_progress_bar(extracted_files, total_files, prefix="Extracting:", suffix="Complete", length=50)
    print(f"\nExtracted linux-{version}")
    if debug:
        print(f"Kernel extracted to linux-{version}")

def apply_patch(version, debug=False):
    apply_patch = input("Do you have a patch file to apply? (yes/no): ").strip().lower()
    if apply_patch == 'yes':
        patch_in_current_dir = input("Is the patch file in the current directory? (yes/no): ").strip().lower()
        if patch_in_current_dir == 'yes':
            patch_files = [f for f in os.listdir('.') if f.endswith('.patch')]
            if patch_files:
                patch_file = patch_files[0]
            else:
                print("No .patch file found in the current directory.")
                return
        else:
            patch_dir = input("Enter the directory containing the patch file: ").strip()
            patch_files = [f for f in os.listdir(patch_dir) if f.endswith('.patch')]
            if patch_files:
                patch_file = os.path.join(patch_dir, patch_files[0])
            else:
                print(f"No .patch file found in the directory {patch_dir}.")
                return
        if debug:
            print(f"Applying patch {patch_file}")
        os.system(f"patch -p1 < {patch_file}")
        print("Patch applied successfully.")

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()

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
                print("Running 'zcat /proc/config.gz > .config'")
            os.system("zcat /proc/config.gz > .config")
            print("Kernel configured with current running kernel's configuration")
            break
        elif config_option == '2':
            if debug:
                print("Running 'make menuconfig'")
            os.system("make menuconfig")
            print("Kernel configuration completed from scratch")
            break
        elif config_option == '3':
            if debug:
                print("Running 'zcat /proc/config.gz > .config' followed by 'make menuconfig'")
            os.system("zcat /proc/config.gz > .config")
            os.system("make menuconfig")
            print("Kernel configuration customized from current running kernel's configuration")
            break
        else:
            print("Invalid selection. Please enter 1, 2, or 3.")

def compile_kernel(version, debug=False):
    if debug:
        print("Running 'make bzImage'")
    os.system("make bzImage")
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
    apply_patch(selected_version, debug)
    configure_kernel(selected_version, debug)
    compile_kernel(selected_version, debug)
    install_kernel(selected_version, debug)
    create_initramfs(selected_version, debug)
    update_bootloader(selected_version, debug)

if __name__ == "__main__":
    main()
