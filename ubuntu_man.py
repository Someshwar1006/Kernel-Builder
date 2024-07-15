import os
import re

GRUB_CFG = "/boot/grub/grub.cfg"

def list_installed_kernels():
    kernels = []
    if os.path.exists(GRUB_CFG):
        with open(GRUB_CFG, 'r') as grub_file:
            for line in grub_file:
                match = re.search(r'vmlinuz-(\S+)', line)
                if match:
                    kernels.append(match.group(1))
    if not kernels:
        print("No kernels installed.")
    else:
        print("Installed kernels:")
        for idx, kernel in enumerate(kernels, start=1):
            print(f"{idx}. {kernel}")
    return kernels

def rename_kernel(kernels):
    list_installed_kernels()
    try:
        idx = int(input("Enter the number of the kernel to rename: ")) - 1
        if idx < 0 or idx >= len(kernels):
            print("Invalid selection.")
            return

        old_name = kernels[idx]
        new_name = input(f"Enter the new name for {old_name}: ")
        old_vmlinuz = f"/boot/vmlinuz-{old_name}"
        new_vmlinuz = f"/boot/vmlinuz-{new_name}"
        if os.path.exists(old_vmlinuz):
            os.rename(old_vmlinuz, new_vmlinuz)
            print(f"Renamed {old_name} to {new_name}.")
        else:
            print(f"{old_vmlinuz} does not exist.")
    except (ValueError, IndexError):
        print("Invalid selection.")

def delete_kernel(kernels):
    list_installed_kernels()
    try:
        idx = int(input("Enter the number of the kernel to delete: ")) - 1
        if idx < 0 or idx >= len(kernels):
            print("Invalid selection.")
            return

        kernel_name = kernels[idx]
        confirm = input(f"Are you sure you want to delete {kernel_name}? (y/N): ")
        if confirm.lower() == 'y':
            vmlinuz = f"/boot/vmlinuz-{kernel_name}"
            initrd = f"/boot/initrd.img-{kernel_name}"
            os.remove(vmlinuz)
            os.remove(initrd)
            print(f"Deleted {kernel_name}.")
        else:
            print("Deletion cancelled.")
    except (ValueError, IndexError):
        print("Invalid selection.")
    except FileNotFoundError as e:
        print(f"Error deleting file: {e}")

def manage_kernels():
    kernels = list_installed_kernels()
    if not kernels:
        return

    print("Manage kernels:")
    print("1. Rename a kernel")
    print("2. Delete a kernel")
    choice = input("Enter your choice: ")

    if choice == '1':
        rename_kernel(kernels)
    elif choice == '2':
        delete_kernel(kernels)
    else:
        print("Invalid choice.")
