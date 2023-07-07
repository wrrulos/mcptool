import dns.resolver


def get_dns_records(hostname, record_type='All'):
    try:
        records_list = []
        records = dns.resolver.resolve(hostname, record_type)

        for record in records:
            records_list.append(record.to_text())

        return records_list

    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
        return None
