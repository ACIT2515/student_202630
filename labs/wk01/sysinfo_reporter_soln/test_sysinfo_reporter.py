from sysinfo_reporter import get_current_user, get_network_info, get_os_info


def test_get_os_info_keys():
    info = get_os_info()
    assert set(info.keys()) == {"system", "release", "version", "machine"}


def test_get_os_info_values_are_strings():
    info = get_os_info()
    assert all(isinstance(value, str) for value in info.values())


def test_get_network_info_keys():
    info = get_network_info()
    assert set(info.keys()) == {"hostname", "ip_address"}


def test_get_network_info_hostname_is_non_empty_string():
    info = get_network_info()
    assert isinstance(info["hostname"], str)
    assert len(info["hostname"]) > 0


def test_get_current_user_returns_non_empty_string():
    user = get_current_user()
    assert isinstance(user, str)
    assert len(user) > 0
