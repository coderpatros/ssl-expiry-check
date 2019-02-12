# SSL Expiry Check

A quick and dirty, but so far functional, script to check SSL certificate expiry.

## Usage

The script reads a file `dns.txt` and checks the SSL certificate expiry for all
listed host names.

The file can be just a list of host names like...
```
    example.com
    example2.com
```

Trailing dots are handled too...
```
    example.com.
    example2.com.
```

It will also handle standard DNS entry text like this...
```
    example.com. 3600 IN A 0.0.0.0
    example2.com. 3600 IN CNAME example.com.
```

It does require the Python OpenSSL module. A quick `pip install pyopenssl`
should take care of it.

After that a `python3 ssl_expiry_check.py` should run the checks.

## Outputs

During the checks results will be printed to the console. In addition several
result files are generated.

`expired.txt` contains a list of host names with expired certificates.  
`expiring-soon.txt` contains a list of host names with certificates expiring
within 120 days.  
`ok.txt` contains a list of host names with certificates that don't expire
within 120 days.  
`failed-checks.txt` contains a list of host names that couldn't be checked
successfully. This could be because the host doesn't have SSL enabled or the
host isn't online.

The result files are only ever appended to. So you should delete them manually
between runs.
