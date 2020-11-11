#!/bin/bash

echo "Packing submission ${1}"

echo "Creating and encrypting key..."
openssl rand -base64 32 > submissions/"${1}".key.bin
openssl rsautl -encrypt -inkey msmarco_doc_public_key.pem -pubin \
  -in submissions/"${1}".key.bin -out submissions/"${1}".key.bin.enc

echo "Encrypting metadata..."
openssl enc -aes-256-cbc -salt -in submissions/"${1}"-metadata.json \
  -out submissions/"${1}"-metadata.json.enc -pass file:submissions/"${1}".key.bin -pbkdf2

echo "Packing tarball..."
cd submissions && tar cvf "${1}".tar "${1}"/ && cd ..

echo "Encrypting submission tarball..."
openssl enc -aes-256-cbc -salt -in submissions/"${1}".tar \
  -out submissions/"${1}".tar.enc -pass file:submissions/"${1}".key.bin -pbkdf2

echo "Done!"
