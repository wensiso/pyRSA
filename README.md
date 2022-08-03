# pyRSA
A RSA program written in Python for educational purposes.

## Usage

```
pyRSA 0.1 
------------------------------
Usage: 
python3 pyrsa.py -e <plaintext_input_file> -o <encripted_output_file> [options]
python3 pyrsa.py -d <encrypted_input_file> -o <plaintext_output_file> [options].

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -e MSG_FILENAME, --encrypt=MSG_FILENAME
                        plaintext input file
  -d ENCRYPT_FILENAME, --decrypt=ENCRYPT_FILENAME
                        encripted text input file
  -o DEST_FILENAME, --output=DEST_FILENAME
                        output file
  -l, --list            pyRSA does not use map-reduce to encrypt or decrypt
                        (it may be slow)
  -k, --keys            generate a new RSA key pair
  -v, --verbose         print plaintext file contents
```
