import datetime
import os
import socket
import ssl
import OpenSSL

cert_date_fmt = r'%Y%m%d%H%M%SZ'


def port_state_description(errno):
    if errno == 0:
        return 'Accepting connections'
    else:
        return os.strerror(errno)

def port_state(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            return sock.connect_ex((host, port))
        except socket.gaierror:
            return None


def certificate_expiry(hostname):
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
                der_cert = sslsock.getpeercert(True)
                pem_cert = ssl.DER_cert_to_PEM_cert(der_cert)          
                x509_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pem_cert)
                notAfter_str = x509_cert.get_notAfter().decode('UTF-8')
                return datetime.datetime.strptime(notAfter_str, cert_date_fmt)
    except (OSError, ssl.CertificateError):
        return None


def valid_days_remaining(hostname):
    expires = certificate_expiry(hostname)
    return expires - datetime.datetime.utcnow()


def output_fields(*fields):
    print(*fields, sep=',')
    with open('/files/output.csv', 'at') as f:
        line = ''
        for field in fields:
            line += str(field) + ','
        line = line.rstrip(',')
        f.write(line + '\n')


if __name__=='__main__':
    output_fields('hostname', 'port_443_state', 'certificate_expiry', 'dns_entry')
    with open('/files/dns.txt', 'rt') as dns_file:
        for dns_entry in dns_file:
            if len(dns_entry.strip()):
                hostname = dns_entry.strip().partition(' ')[0].rstrip('.')
                
                state = port_state(hostname, 443)

                expiry = None
                if state == 0:
                    expiry = certificate_expiry(hostname)
                
                if state is None:
                    state_str = 'Unknown host'
                else:
                    state_str = port_state_description(state)

                if state != 0 and port_state(hostname, 80) == 0:
                    state_str += ' (but accepting connections on port 80)'

                expiry_str = str(expiry)
                if expiry is None and state == 0 :
                    expiry_str = 'Certificate invalid'

                output_fields(hostname, state_str, expiry_str, dns_entry.strip())
