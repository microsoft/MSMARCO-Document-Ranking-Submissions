#!/bin/bash

echo "Unpacking submission ${1}"

echo "Decrypting key..."
openssl rsautl -decrypt -inkey msmarco_doc_private_key.pem \
  -in submissions/"${1}".key.bin.enc -out submissions/"${1}".key.bin

echo "Decrypting metadata..."
openssl enc -d -aes-256-cbc -in submissions/"${1}"-metadata.json.enc \
  -out submissions/"${1}"-metadata.json -pass file:submissions/"${1}".key.bin -pbkdf2

echo "Decrypting submission tarball..."
openssl enc -d -aes-256-cbc -in submissions/"${1}".tar.enc \
  -out submissions/"${1}".tar -pass file:submissions/"${1}".key.bin -pbkdf2

echo "Unpacking tarball..."
tar xf submissions/"${1}".tar -C submissions/

echo "Done!"
