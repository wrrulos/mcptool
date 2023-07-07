from utils.managers.config_manager import config_manager


def get_scan_command(scan_method, target, ports):
    """
    Create the command needed to scan.

    Args:
        scan_method (str): Scan method.
        target (str): Target to scan.
        ports (str): Ports range.

    Returns:
        str: Scan command.
    """

    if scan_method == 'nmap':
        command = config_manager.config['scannerOptions']['nmapCommand'].replace('[0]', ports).replace('[1]', target)

    if scan_method == 'old_quboscanner':
        command = config_manager.config['scannerOptions']['oldQuboCommand'].replace('[0]', target).replace('[1]', ports).replace('[2]', config_manager.config['scannerOptions']['quboThreads']).replace('[3]', config_manager.config['scannerOptions']['quboTimeout'])

    #if scan_method == 'new_quboscanner':
    #    pass

    if scan_method == 'masscan':
        command = config_manager.config['scannerOptions']['masscanCommand'].replace('[0]', target).replace('[1]', ports)

    return command
