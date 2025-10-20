#!/usr/bin/python3

import requests
import argparse
import sys
from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize colorama for coloring
init(autoreset=True)


# Define a function to fetch the calling convention for an architecture
def get_calling_convention(arch):
    url = f"https://api.syscall.sh/v1/conventions/{arch}"
    response = requests.get(url, headers={"accept": "application/json"})

    if response.status_code == 200:
        data = response.json()

        # Prepare the data for horizontal tabulation (values as columns)
        headers = list(data.keys())
        values = list(data.values())

        # Beautify output with tabulate and color
        print(Fore.CYAN + f"\nCalling Convention for {arch.lower()}:\n")

        header_style = [
            Style.BRIGHT + Fore.LIGHTCYAN_EX + header + Style.RESET_ALL
            for header in headers
        ]
        # The remaining rows will be normal text
        normal_row_style = [Fore.GREEN] * len(values)

        print(
            tabulate(
                [values],
                headers=header_style,
                tablefmt="grid",
                stralign="center",
                numalign="center",
            )
        )

    else:
        print(
            Fore.RED
            + f"Error fetching data for architecture {arch}. Status Code: {response.status_code}"
        )


# Define a function to fetch syscall details for a given syscall name
def get_syscall_details(syscall, arch=None):
    url = f"https://api.syscall.sh/v1/syscalls/{syscall}"
    response = requests.get(url, headers={"accept": "application/json"})

    if response.status_code == 200:
        data = response.json()

        # If it's a list (multiple architectures)
        if isinstance(data, list):
            if arch:
                # Filter by architecture (case-insensitive)
                data = [
                    item
                    for item in data
                    if item.get("arch", "").lower() == arch.lower()
                ]
                if not data:
                    print(
                        Fore.RED
                        + f"No syscall entry found for '{syscall}' on architecture '{arch}'."
                    )
                    return

            print(Fore.CYAN + f"\nSyscall details for {syscall}:")
            for item in data:
                headers = list(item.keys())
                values = list(item.values())
                header_style = [
                    Style.BRIGHT + Fore.LIGHTCYAN_EX + header + Style.RESET_ALL
                    for header in headers
                ]
                print(
                    tabulate(
                        [values],
                        headers=header_style,
                        tablefmt="grid",
                        stralign="center",
                        numalign="center",
                    )
                )
        else:
            # Single object (non-list)
            headers = list(data.keys())
            values = list(data.values())
            header_style = [
                Style.BRIGHT + Fore.LIGHTCYAN_EX + header + Style.RESET_ALL
                for header in headers
            ]
            print(Fore.CYAN + f"\nSyscall details for {syscall}:")
            print(
                tabulate(
                    [values],
                    headers=header_style,
                    tablefmt="grid",
                    stralign="center",
                    numalign="center",
                )
            )
    else:
        print(
            Fore.RED
            + f"Error fetching syscall data for {syscall}. Status Code: {response.status_code}"
        )


# Main function
def main():
    parser = argparse.ArgumentParser(
        description="Fetch calling convention or syscall details"
    )
    # Add flags for architecture and syscall
    parser.add_argument(
        "-a",
        "--arch",
        choices=["x86", "x64", "arm", "arm64"],
        help="Architecture (x86, x64, arm, arm64)",
    )
    parser.add_argument("-s", "--syscall", help="Syscall name (optional, e.g., execve)")

    args = parser.parse_args()

    # If neither architecture nor syscall is provided, show usage
    if not args.arch and not args.syscall:
        print(
            Fore.RED
            + "Error: You must provide either an architecture or a syscall. Use -h/--help to get help."
        )
        sys.exit(1)

    # If architecture is provided, fetch calling convention
    if args.arch:
        get_calling_convention(args.arch)

    # If syscall is provided, fetch syscall details
    if args.syscall:
        get_syscall_details(args.syscall, args.arch)


if __name__ == "__main__":
    main()
