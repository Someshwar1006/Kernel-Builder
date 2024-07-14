<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Linux Kernel Builder</title>
</head>

<body>
    <h1>Linux Kernel Builder</h1>

    <p>Linux Kernel Builder simplifies the process of compiling and installing the Linux kernel on various distributions,
        including Arch Linux and Ubuntu/Debian.</p>

    <h2>Description</h2>
    <p>This tool automates kernel version selection, patch application, configuration, compilation, and installation,
        optimizing the process for efficiency and customization.</p>

    <h2>Features</h2>
    <ul>
        <li><strong>Automatic Version Detection:</strong> Fetches available Linux kernel versions from kernel.org.</li>
        <li><strong>Interactive Selection:</strong> Allows users to select a kernel version to build.</li>
        <li><strong>Download and Extraction:</strong> Downloads and extracts the selected kernel version.</li>
        <li><strong>Configuration Options:</strong> Offers various methods: default, from scratch, or customization.</li>
        <li><strong>Patch Application:</strong> Supports applying patch files before compilation.</li>
        <li><strong>Compilation and Installation:</strong> Compiles the kernel, installs it, creates an initramfs, and
            updates the bootloader.</li>
    </ul>

    <h2>Supported Distributions</h2>
    <ul>
        <li>Arch Linux</li>
        <li>Ubuntu/Debian</li>
        <!-- Add other distributions here if applicable -->
    </ul>

    <h2>Requirements</h2>
    <ul>
        <li>Python 3.x</li>
        <li><code>requests</code> library (for downloading)</li>
        <li>Standard Unix tools (<code>tar</code>, <code>patch</code>, etc.)</li>
    </ul>

    <h2>Usage</h2>
    <ol>
        <li>Clone the repository:</li>
        <pre><code>git clone https://github.com/your-username/linux-kernel-builder.git
cd linux-kernel-builder</code></pre>
        <li>Run the application:</li>
        <pre><code>python main.py</code></pre>
        <li>Follow the prompts to select a kernel version, configure options, apply patches (if any), and complete the
            build process.</li>
    </ol>

    <h2>Configuration Options</h2>
    <ul>
        <li><strong>Debug Mode:</strong> Enable debug mode for verbose output during each step of the process.</li>
    </ul>

    <h2>License</h2>
    <p>This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for details.</p>

    <h2>Acknowledgments</h2>
    <ul>
        <li>Built using Python and standard Unix tools.</li>
        <li>Inspired by the need to simplify the Linux kernel compilation process.</li>
    </ul>

    <h2>Contributing</h2>
    <ol>
        <li>Fork the repository.</li>
        <li>Create your feature branch (<code>git checkout -b feature/new-feature</code>).</li>
        <li>Commit your changes (<code>git commit -am 'Add some feature'</code>).</li>
        <li>Push to the branch (<code>git push origin feature/new-feature</code>).</li>
        <li>Create a new Pull Request.</li>
    </ol>

</body>

</html>
