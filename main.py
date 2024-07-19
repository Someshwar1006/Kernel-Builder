#!/usr/bin/env python3
import argparse
import arch
import ubuntu
import arch_man
import ubuntu_man
import time
import distro

def display_author_info():
    author_name = "Someshwar S, Harshavardhan S"
    print(f"Author and Maintainer: {author_name}")
    time.sleep(3)  # Display for 3 seconds
    print("\033[H\033[J")  # Clear the screen (works on Unix-like systems)

def install_kernel(distro_module, debug):
    available_versions = distro_module.get_available_versions(debug)
    if not available_versions:
        return

    selected_version = distro_module.choose_kernel_version(available_versions, debug)

    distro_module.install_packages(debug)
    distro_module.download_kernel(selected_version, debug)
    distro_module.extract_kernel(selected_version, debug)
    distro_module.apply_patch(selected_version, debug)
    distro_module.configure_kernel(selected_version, debug)
    distro_module.compile_kernel(selected_version, debug)
    distro_module.install_kernel(selected_version, debug)
    distro_module.create_initramfs(selected_version, debug)
    distro_module.update_bootloader(selected_version, debug)

def main():
    display_author_info()  # Display author info for 3 seconds

    parser = argparse.ArgumentParser(description="Linux Kernel Builder")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    #parser.add_argument('--distro', choices=['arch', 'ubuntu'])
    args = parser.parse_args()
    debug = args.debug
    #distroc = args.distro

    print(distro.id())

    if distro.id() == 'arch':
        distro_module = arch
        manage_module = arch_man
    elif distro.id() == 'ubuntu':
        distro_module = ubuntu
        manage_module = ubuntu_man
    else:
        print("Unsupported distribution.")
        return

    print("1. Install a new kernel")
    print("2. Manage existing kernels")
    choice = input("Enter your choice: ")

    if choice == '1':
        install_kernel(distro_module, debug)
    elif choice == '2':
        print()
        manage_module.manage_kernels()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
