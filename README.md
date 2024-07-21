# Kernel Builder

`kernel-builder` is a Python-based tool designed to help users manage Linux kernels on their systems. It provides functionalities to list, rename, delete, and build kernels, making it a versatile tool for kernel management.

## Features

### Kernel Management

- **List Installed Kernels:**
  - Display all kernels currently installed on your system.
  - Shows kernel versions extracted from the GRUB configuration file.

- **Rename Existing Kernels:**
  - Select a kernel from the list of installed kernels.
  - Provide a new name to rename the selected kernel.
  - The tool handles renaming the kernel image files.

- **Delete Old Kernels:**
  - Select a kernel from the list to be deleted.
  - Confirm the deletion process.
  - Removes kernel image files and associated initrd files.

### Kernel Building and Installation

- **Install Prerequisite Packages:**
  - Installs necessary packages and dependencies for kernel building (e.g., `build-essential`, `libncurses-dev`, `bison`, etc.).

- **Fetch Available Kernel Versions:**
  - Retrieves a list of available kernel versions from kernel.org.

- **Choose Kernel Version:**
  - Allows you to select a specific kernel version to build from the list of available versions.

- **Download Kernel Source:**
  - Downloads the selected kernel version’s source code from kernel.org.

- **Extract Kernel Source:**
  - Extracts the downloaded kernel source archive.

- **Apply Patches (Optional):**
  - Provides an option to apply a patch file to the kernel source.
  - Supports applying patches from the current directory or a specified directory.

- **Configure Kernel:**
  - Offers options to configure the kernel:
    - Use the default configuration (`make localmodconfig`).
    - Configure from scratch (`make menuconfig`).
    - Customize from the default configuration (both `localmodconfig` and `menuconfig`).

- **Compile Kernel:**
  - Compiles the kernel using multiple cores for faster build times.

- **Install Kernel:**
  - Installs the compiled kernel and modules.

- **Update Bootloader:**
  - Updates the bootloader configuration to include the new kernel.

## Installation

### Arch Linux / AUR

To install `kernel-builder` on Arch Linux using the AUR, follow these steps:

1. **Ensure you have an AUR helper installed** (e.g., `yay`).
2. **Install `kernel-builder` using `yay`:**

    ```bash
    yay -S kernel-builder
    ```

### Ubuntu

To use `kernel-builder` on Ubuntu, follow these steps:

1. **Install Python and necessary dependencies:**

    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
    ```

2. **Clone the repository or download the `kernel-builder` files.**

3. **Navigate to the `kernel-builder` directory:**

    ```bash
    cd path/to/kernel-builder

4. **Run the main script:**

    ```bash
    python3 main.py
    ```

## Usage

### Managing Kernels

1. **List Installed Kernels:**
   - Execute the script and choose the option to list kernels.
   - View the list of installed kernels and their versions.

2. **Rename a Kernel:**
   - Choose the kernel to rename from the list.
   - Enter the new name for the selected kernel.
   - The script renames the kernel image file accordingly.

3. **Delete a Kernel:**
   - Select the kernel to delete from the list.
   - Confirm the deletion to remove the kernel image and initrd files.

### Building and Installing a New Kernel

1. **Install Prerequisite Packages:**
   - Ensure all required packages are installed.

2. **Get Available Kernel Versions:**
   - Fetch the list of kernel versions from kernel.org.

3. **Select and Download a Kernel Version:**
   - Choose the kernel version you wish to build and download it.

4. **Extract, Patch, and Configure the Kernel:**
   - Extract the downloaded kernel source.
   - Apply patches if necessary.
   - Configure the kernel using one of the provided options.

5. **Compile and Install the Kernel:**
   - Compile the kernel using available cores.
   - Install the kernel and its modules.

6. **Update the Bootloader:**
   - Update the bootloader configuration to include the new kernel.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
