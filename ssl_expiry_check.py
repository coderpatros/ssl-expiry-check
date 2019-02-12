import datetime
import socket
import ssl
import OpenSSL

cert_date_fmt = r'%Y%m%d%H%M%SZ'


def certificate_expiry(hostname):
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
            der_cert = sslsock.getpeercert(True)
            pem_cert = ssl.DER_cert_to_PEM_cert(der_cert)          
            x509_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pem_cert)
            notAfter_str = x509_cert.get_notAfter().decode('UTF-8')
            return datetime.datetime.strptime(notAfter_str, cert_date_fmt)


def valid_days_remaining(hostname):
    expires = certificate_expiry(hostname)
    return expires - datetime.datetime.utcnow()


if __name__=='__main__':
    with open('dns.txt', 'rt') as dns_file:
        for dns_entry in dns_file:
            if len(dns_entry.strip()):
                hostname = dns_entry.strip().partition(' ')[0].rstrip('.')
                print('Checking', hostname, end='')
                try:
                    days_remaining = valid_days_remaining(hostname)
                    if days_remaining < datetime.timedelta(days=0):
                        print(' *** CERTIFICATE ALREADY EXPIRED ***')
                        open('expired.txt', 'at').write(hostname + '\n')
                    elif days_remaining < datetime.timedelta(days=120):
                        print(' CERTIFICATE EXPIRING SOON')
                        open('expiring-soon.txt', 'at').write(hostname + '\n')
                    else:
                        print(' EXPIRY OK')
                        open('ok.txt', 'at').write(hostname + '\n')
                except (OSError, ssl.CertificateError):
                    print(' *** CHECK FAILED ***')
                    open('failed-checks.txt', 'at').write(hostname + '\n')
