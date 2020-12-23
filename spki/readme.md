Just run
`docker build . -t spki:test && docker run --rm  -v $PWD/local/spki:/spki/ca/  -it spki:test`