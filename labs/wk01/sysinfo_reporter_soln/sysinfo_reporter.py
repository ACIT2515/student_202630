"""SysInfo Reporter - print a read-only summary of the local host."""

import getpass as gp
import platform
import socket


def get_os_info() -> dict[str, str]:
    """Return operating system information for the local host.

    Returns:
        A dictionary with the keys "system", "release", "version", and
        "machine".

    Examples:
        >>> info = get_os_info()
        >>> sorted(info.keys())
        ['machine', 'release', 'system', 'version']
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
    }


def get_network_info() -> dict[str, str]:
    """Return basic network identity information for the local host.

    Uses socket.gethostname() to find the computer's name, and
    socket.gethostbyname() to resolve it to a local IP address. If the
    hostname cannot be resolved, "ip_address" is set to "unknown" instead of
    raising an exception.

    Returns:
        A dictionary with the keys "hostname" and "ip_address".

    Examples:
        >>> info = get_network_info()
        >>> sorted(info.keys())
        ['hostname', 'ip_address']
    """
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip_address = "unknown"
    return {"hostname": hostname, "ip_address": ip_address}


def get_current_user() -> str:
    """Return the username of the person currently logged in.

    Returns:
        The current user's login name.

    Examples:
        >>> isinstance(get_current_user(), str)
        True
    """
    return gp.getuser()


def main() -> None:
    """Print a summary of the local host."""
    os_info = get_os_info()
    network_info = get_network_info()
    user = get_current_user()

    print("Host Summary")
    print("=" * 40)
    print(f"Computer name: {network_info['hostname']}")
    print(f"IP address:    {network_info['ip_address']}")
    print(f"Operating system: {os_info['system']} {os_info['release']}")
    print(f"Machine type:  {os_info['machine']}")
    print(f"Current user:  {user}")


if __name__ == "__main__":
    main()
