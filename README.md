# ATEC608

This repository contains the example snippets for using the ATECC608. 

## Build and Run
```
docker build -t ecc608 . && docker run --device=/dev/i2c-1 ecc608
```

To run different files, make sure to change the `CMD` in the `Dockerfile` to the desired file.