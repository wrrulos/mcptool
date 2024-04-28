class GetCloudflareIps:
    def __init__(self) -> None:
        self.cloudflare_ips: list = ['104.16.', '104.17.', '104.18.', '104.19.', '104.20.', '104.21.', '104.22.', '104.23.', '104.24.', '104.25.', '104.26.', '104.27.', '104.28.', '104.29.', '104.30.', '104.31.', '172.64.', '172.65.', '172.66.', '172.67.', '172.68.', '172.69.', '172.70.', '172.71.', '1.1.1.1']

    def get(self, ips: list) -> list:
        """
        Get Cloudflare IPs from a list of IPs

        Args:
            ips (list): List of IPs

        Returns:
            list: List of Cloudflare IPs
        """

        cloudflare_ips: list = []

        for ip in ips:
            for cloudflare_ip in self.cloudflare_ips:
                if cloudflare_ip in ip:
                    cloudflare_ips.append(ip)
                    break

        return cloudflare_ips
