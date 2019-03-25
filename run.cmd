docker build --tag ssl-expiry-check .
docker run -v `pwd`:/files -it ssl-expiry-check