# Linux Kernel Builder

Linux Kernel Builder simplifies the process of compiling and installing the Linux kernel on various distributions, including Arch Linux and Ubuntu/Debian.

## Description

This tool automates kernel version selection, patch application, configuration, compilation, and installation, optimizing the process for efficiency and customization.

## Features

- **Automatic Version Detection:** Fetches available Linux kernel versions from kernel.org.
- **Interactive Selection:** Allows users to select a kernel version to build.
- **Download and Extraction:** Downloads and extracts the selected kernel version.
- **Configuration Options:** Offers various methods: default, from scratch, or customization.
- **Patch Application:** Supports applying patch files before compilation.
- **Compilation and Installation:** Compiles the kernel, installs it, creates an initramfs, and updates the bootloader.

## Supported Distributions

- Arch Linux
- Ubuntu/Debian
- *(Add other distributions here if applicable)*

## Requirements

- Python 3.x
- `requests` library (for downloading)
- Standard Unix tools (`tar`, `patch`, etc.)

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/linux-kernel-builder.git
   cd linux-kernel-builder
   ```

2. Run the application:

   ```bash
   python main.py
   ```

3. Follow the prompts to select a kernel version, configure options, apply patches (if any), and complete the build process.

## Configuration Options

- **Debug Mode:** Enable debug mode for verbose output during each step of the process.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built using Python and standard Unix tools.
- Inspired by the need to simplify the Linux kernel compilation process.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a new Pull Request.
