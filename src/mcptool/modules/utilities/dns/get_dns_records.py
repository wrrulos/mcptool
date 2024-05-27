import dns


class GetDNSRecords:
    def __init__(self, domain):
        self.domain = domain
        self.dns_records_to_look_up: list = [
            'A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA',
            'SRV', 'TXT', 'CAA', 'SPF', 'NAPTR'
        ]

    def get_dns_records(self) -> list:
        """
        Method to get the DNS records of a domain

        Returns:
            list: The DNS records of the domain
        """

        dns_records = []

        for dns_record in self.dns_records_to_look_up:
            try:
                dns_record_value = dns.resolver.resolve(self.domain, dns_record)
                dns_records.append({
                    'type': dns_record,
                    'value': [str(record) for record in dns_record_value]
                })

            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
                pass

        return dns_records
