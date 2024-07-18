#!/usr/bin/env python3
import argparse
import subprocess
import time
import os

def display_author_info():
    author_name = "Someshwar S"
    print(f"Author and Maintainer: {author_name}")
    time.sleep(3)  # Display for 3 seconds
    print("\033[H\033[J")  # Clear the screen (works on Unix-like systems)

def run_script(script_name, args):
    command = ['python3', script_name] + args
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}", file=sys.stderr)

def main():
    display_author_info()  # Display author info for 3 seconds

    parser = argparse.ArgumentParser(description="Linux Kernel Builder")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--distro', choices=['arch', 'ubuntu'], default='arch', help='Linux distribution (default: arch)')
    args = parser.parse_args()

    debug = args.debug
    distro = args.distro

    if distro == 'arch':
        script_name = 'arch.py'
    elif distro == 'ubuntu':
        script_name = 'ubuntu.py'
    else:
        print("Unsupported distribution.")
        return

    print("1. Install a new kernel")
    print("2. Manage existing kernels")
    choice = input("Enter your choice: ")

    if choice == '1':
        run_script(script_name, ['install_kernel', '--debug' if debug else ''])
    elif choice == '2':
        run_script(script_name, ['manage_kernels'])
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
