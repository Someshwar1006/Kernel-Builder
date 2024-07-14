import os
import requests
import subprocess
import tarfile

# ANSI color escape sequences.
class colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

KERNEL_BASE_URL = "https://www.kernel.org"

def get_available_versions(debug=False):
    url = f"{KERNEL_BASE_URL}/releases.json"
    if debug:
        print(f"{colors.DARKCYAN}Fetching available versions from {url}{colors.END}")
    response = requests.get(url)
    if response.status_code == 200:
        versions = response.json().get('releases')
        if debug:
            print(f"{colors.GREEN}Fetched {len(versions)} versions{colors.END}")
        return versions
    else:
        print(f"{colors.RED}Failed to fetch kernel versions. Check your internet connection.{colors.END}")
        return []

def format_version_info(version_info):
    version = version_info.get('version', 'Unknown Version')
    released_date = version_info.get('released', {}).get('isodate', 'Unknown Date')
    source_url = version_info.get('source', 'Unknown Source')
    return f"{colors.BOLD}{version}{colors.END} - Released: {released_date}\n   Source: {source_url}"

def choose_kernel_version(versions, debug=False):
    print(f"{colors.PURPLE}Available Linux Kernel Versions:{colors.END}")
    for idx, version_info in enumerate(versions, start=1):
        formatted_info = format_version_info(version_info)
        print(f"{idx}. {formatted_info}")

    while True:
        try:
            selection = input("Enter the number of the kernel version to build: ")
            index = int(selection) - 1
            if 0 <= index < len(versions):
                if debug:
                    print(f"{colors.GREEN}Selected version: {versions[index].get('version')}{colors.END}")
                return versions[index].get('version')
            else:
                print(f"{colors.RED}Invalid selection. Please enter a number from the list.{colors.END}")
        except ValueError:
            print(f"{colors.RED}Invalid input. Please enter a number.{colors.END}")

def download_kernel(version, debug=False):
    url = f"{KERNEL_BASE_URL}/pub/linux/kernel/v{version.split('.')[0]}.x/linux-{version}.tar.xz"
    if debug:
        print(f"{colors.CYAN}Downloading kernel from {url}{colors.END}")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        with open(f"linux-{version}.tar.xz", 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    print_progress_bar(downloaded_size, total_size, prefix=f"{colors.BLUE}Downloading:{colors.END}", suffix=f"{colors.GREEN}Complete{colors.END}", length=50)
        print(f"\nDownloaded linux-{version}.tar.xz")
        if debug:
            print(f"{colors.GREEN}Kernel downloaded to linux-{version}.tar.xz{colors.END}")
    else:
        print(f"{colors.RED}Failed to download kernel. Check the version and try again.{colors.END}")

def extract_kernel(version, debug=False):
    if debug:
        print(f"{colors.CYAN}Extracting linux-{version}.tar.xz{colors.END}")
    with tarfile.open(f"linux-{version}.tar.xz", 'r:xz') as tar:
        total_files = len(tar.getmembers())
        extracted_files = 0
        for member in tar.getmembers():
            tar.extract(member)
            extracted_files += 1
            print_progress_bar(extracted_files, total_files, prefix=f"{colors.BLUE}Extracting:{colors.END}", suffix=f"{colors.GREEN}Complete{colors.END}", length=50)
    print(f"\nExtracted linux-{version}")
    if debug:
        print(f"{colors.GREEN}Kernel extracted to linux-{version}{colors.END}")

def apply_patch(version, debug=False):
    apply_patch = input(f"{colors.YELLOW}Do you have a patch file to apply? (yes/no): {colors.END}").strip().lower()
    if apply_patch == 'yes':
        patch_in_current_dir = input(f"{colors.YELLOW}Is the patch file in the current directory? (yes/no): {colors.END}").strip().lower()
        if patch_in_current_dir == 'yes':
            patch_files = [f for f in os.listdir('.') if f.endswith('.patch')]
            if patch_files:
                patch_file = patch_files[0]
            else:
                print(f"{colors.RED}No .patch file found in the current directory.{colors.END}")
                return
        else:
            patch_dir = input(f"{colors.YELLOW}Enter the directory containing the patch file: {colors.END}").strip()
            patch_files = [f for f in os.listdir(patch_dir) if f.endswith('.patch')]
            if patch_files:
                patch_file = os.path.join(patch_dir, patch_files[0])
            else:
                print(f"{colors.RED}No .patch file found in the directory {patch_dir}.{colors.END}")
                return
        if debug:
            print(f"{colors.CYAN}Applying patch {patch_file}{colors.END}")
        os.system(f"patch -p1 < {patch_file}")
        print(f"{colors.GREEN}Patch applied successfully.{colors.END}")

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()

def configure_kernel(version, debug=False):
    os.chdir(f"linux-{version}")
    print(f"{colors.PURPLE}Configuration options:{colors.END}")
    print(f"{colors.BOLD}1.{colors.END} Use default configuration")
    print(f"{colors.BOLD}2.{colors.END} Choose configuration from scratch")
    print(f"{colors.BOLD}3.{colors.END} Customize from default configuration")
    while True:
        config_option = input(f"{colors.YELLOW}Enter your choice (1/2/3): {colors.END}")
        if config_option == '1':
            if debug:
                print(f"{colors.CYAN}Running 'zcat /proc/config.gz > .config'{colors.END}")
            os.system("zcat /proc/config.gz > .config")
            print(f"{colors.GREEN}Kernel configured with current running kernel's configuration{colors.END}")
            break
        elif config_option == '2':
            if debug:
                print(f"{colors.CYAN}Running 'make menuconfig'{colors.END}")
            os.system("make menuconfig")
            print(f"{colors.GREEN}Kernel configuration completed from scratch{colors.END}")
            break
        elif config_option == '3':
            if debug:
                print(f"{colors.CYAN}Running 'zcat /proc/config.gz > .config' followed by 'make menuconfig'{colors.END}")
            os.system("zcat /proc/config.gz > .config")
            os.system("make menuconfig")
            print(f"{colors.GREEN}Kernel configuration customized from current running kernel's configuration{colors.END}")
            break
        else:
            print(f"{colors.RED}Invalid selection. Please enter 1, 2, or 3.{colors.END}")
    os.chdir("..")

def compile_kernel(version, debug=False):
    print(f"{colors.CYAN}Compiling kernel{colors.END}")
    subprocess.run(["make", "bzImage"])

def install_kernel(version, debug=False):
    print(f"{colors.CYAN}Installing kernel{colors.END}")
    subprocess.run(["sudo", "make", "modules_install"])
    subprocess.run(["sudo", "make", "install"])

def create_initramfs(version, debug=False):
    print(f"{colors.CYAN}Creating initramfs{colors.END}")
    subprocess.run(["sudo", "mkinitcpio", "-k", version, "-c", "/etc/mkinitcpio.conf", "-g", "/boot/initramfs-linux.img"])

def update_bootloader(version, debug=False):
    print(f"{colors.CYAN}Updating bootloader{colors.END}")
    os.system("sudo update-grub")
    print(f"{colors.GREEN}Bootloader updated{colors.END}")
