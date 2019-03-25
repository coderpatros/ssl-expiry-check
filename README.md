# SSL Expiry Check

A quick and dirty, but so far functional, script to check SSL certificate expiry.

## DNS entries

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

## Usage

    docker build --tag ssl-expiry-check .
    docker run -v `pwd`:/files -it ssl-expiry-check

Or just execute `run.cmd` which will run the two commands above.

## Output

All output will be displayed in the console and written to `output.csv`.

`output.csv` is only appended to. So you need to delete it to start a clean run.
