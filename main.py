#!/usr/bin/env python3
import argparse
import arch
import ubuntu
import time

def display_author_info():
    author_name = "Someshwar S"
    print(f"Author and Maintainer: {author_name}")
    time.sleep(3)  # Display for 3 seconds
    print("\033[H\033[J")  # Clear the screen (works on Unix-like systems)

def main():
    display_author_info()  # Display author info for 3 seconds

    parser = argparse.ArgumentParser(description="Linux Kernel Builder")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--distro', choices=['arch', 'ubuntu'], default='arch', help='Linux distribution (default: arch)')
    args = parser.parse_args()

    debug = args.debug
    distro = args.distro

    if distro == 'arch':
        distro_module = arch
    elif distro == 'ubuntu':
        distro_module = ubuntu
    else:
        print("Unsupported distribution.")
        return

    available_versions = distro_module.get_available_versions(debug)
    if not available_versions:
        return

    selected_version = distro_module.choose_kernel_version(available_versions, debug)

    distro_module.download_kernel(selected_version, debug)
    distro_module.extract_kernel(selected_version, debug)
    distro_module.apply_patch(selected_version, debug)
    distro_module.configure_kernel(selected_version, debug)
    distro_module.compile_kernel(selected_version, debug)
    distro_module.install_kernel(selected_version, debug)
    distro_module.create_initramfs(selected_version, debug)
    distro_module.update_bootloader(selected_version, debug)

if __name__ == "__main__":
    main()
