# Maintainer: Someshwar S <someshwar1006@gmail.com>
pkgname=kernel-builder
pkgver=1.0
pkgrel=1
pkgdesc="Simplifies Linux kernel compilation with version selection, patching, and configuration options for Arch Linux and Ubuntu/Debian, enhancing installation efficiency and customization."
arch=('any')
url="https://github.com/Someshwar1006/Kernel-Builder"
license=('MIT')
depends=('python3')
source=("https://github.com/Someshwar1006/Kernel-Builder/blob/main/kernel-builder-1.0.tar.gz")
sha256sums=('035cbfd12831a3a35d01ea7b0353fe0e92e123f3df7f474a31cbccceb16a7b28')

package() {
    cd "${srcdir}/Kernel-Builder-${pkgver}"

    # Install Python scripts
    install -Dm644 main.py "${pkgdir}/usr/share/kernel-builder/main.py"
    install -Dm644 arch.py "${pkgdir}/usr/share/kernel-builder/arch.py"
    install -Dm644 ubuntu.py "${pkgdir}/usr/share/kernel-builder/ubuntu.py"

    # Install license and README
    install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
    install -Dm644 README.md "${pkgdir}/usr/share/doc/${pkgname}/README.md"
}
