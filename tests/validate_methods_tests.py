import pytest

from mcptool.modules.utilities.commands.validate import ValidateArgument


def test_is_domain():
    """
    Test if the given string is a domain
    """

    assert ValidateArgument.is_domain('google.com') == True
    assert ValidateArgument.is_domain('google') == False
    assert ValidateArgument.is_domain('google.') == False
    assert ValidateArgument.is_domain('127.0.0.1') == False


def test_is_ip_address():
    """
    Test if the given string is an IP address
    """

    assert ValidateArgument.is_ip_address('127.0.0.1') == True
    assert ValidateArgument.is_ip_address('127.0.0') == False
    assert ValidateArgument.is_ip_address('127.0.0.256') == False


def test_is_ip_and_port():
    """
    Test if the given string is an IP and port
    """

    assert ValidateArgument.is_ip_and_port('127.0.0.1:25565') == True
    assert ValidateArgument.is_ip_and_port('127.0.0.1:25565:25565') == False
    assert ValidateArgument.is_ip_and_port('127.0.0.1') == False


def test_is_port_range_py_method():
    """
    Test if the given string is a port range
    """

    assert ValidateArgument.is_port_range_py_method('25565') == True
    assert ValidateArgument.is_port_range_py_method('25565-25566') == True
    assert ValidateArgument.is_port_range_py_method('25565-') == False
    assert ValidateArgument.is_port_range_py_method('25565-65536') == False


def test_is_seeker_subcommand():
    """
    Test if the given string is a Seeker subcommand
    """

    assert ValidateArgument.is_seeker_subcommand('token') == True
    assert ValidateArgument.is_seeker_subcommand('servers') == True
    assert ValidateArgument.is_seeker_subcommand('invalid') == False


def test_is_scan_method():
    """
    Test if the given string is a scan method
    """

    assert ValidateArgument.is_scan_method('nmap') == True
    assert ValidateArgument.is_scan_method('qubo') == True
    assert ValidateArgument.is_scan_method('masscan') == True
    assert ValidateArgument.is_scan_method('py') == True
    assert ValidateArgument.is_scan_method('invalid') == False


def test_is_yes_no():
    """
    Test if the given string is a yes or no
    """

    assert ValidateArgument.is_yes_no('y') == True
    assert ValidateArgument.is_yes_no('n') == True
    assert ValidateArgument.is_yes_no('invalid') == False


def test_is_proxy_type():
    """
    Test if the given string is a proxy type
    """

    assert ValidateArgument.is_proxy_type('waterfall') == True
    assert ValidateArgument.is_proxy_type('velocity') == True
    assert ValidateArgument.is_proxy_type('invalid') == False


def test_is_velocity_forwading_mode():
    """
    Test if the given string is a velocity forwarding mode
    """

    assert ValidateArgument.is_velocity_forwading_mode('none') == True
    assert ValidateArgument.is_velocity_forwading_mode('legacy') == True
    assert ValidateArgument.is_velocity_forwading_mode('bungeeguard') == True
    assert ValidateArgument.is_velocity_forwading_mode('modern') == True
    assert ValidateArgument.is_velocity_forwading_mode('invalid') == False