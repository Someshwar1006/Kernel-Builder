import argparse
import arch
import ubuntu
import time
import curses

def display_author_info(stdscr):
    author_name = "Someshwar S"

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    stdscr.attron(curses.color_pair(1))
    stdscr.clear()
    stdscr.addstr(0, 0, f"Author and Maintainer: {author_name}", curses.color_pair(1))
    stdscr.refresh()
    stdscr.attroff(curses.color_pair(1))
    time.sleep(3)  # Display for 3 seconds

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    display_author_info(stdscr)  # Display author info for 3 seconds

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
    curses.wrapper(main)
