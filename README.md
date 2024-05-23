# Encrypt Store

A simple script to encrypt and store your passwords

## Installation

```bash
pip install -r requirements.txt
```

and then run the script

```bash
python main.py
```

maybe make an alias that activates the venv, runs the script and then deactivates the venv

## Info

- Simple stuff (read the script yourself)
- DON'T FORGET YOUR ENC_PASSWORD !!!! (NON RECOVERABLE)
- USE THE SAME ENC_PASSWORD for encrypting all you passwords (or else you'll have to remember multiple enc_passwords)
- you'll need to remember the enc_password used for encryption to decrypt ... else its gone ... say bye bye to your passwords

## Change encryption key ?

- Keeping it simple .... you cant (currently), youll need to delete all passwords and re-enter them with a new key

## Safe ?

- These encrypted passwords can be stored anywhere, just dont store your encryption key ON THE INTERNET!!!

## Advanced Options

- After startup, input choice as `0` to see advanced options
- Advanced options include:
  - `init` : not useful to you
  - `export` : export all passwords to a gzip file in `pwd` (it'll tell you where the gzip was created)
  - `import` : i didn't need it now ... so i didn't implement

## Why am i doing this ?

- I dont trust myself (to remember passwords)
- I dont trust google docs/ whatever online docs (cause big corp will have your passwords)
- I dont trust password managers (who the hell knows whats going on in those applications???)
- Hence the simple script that creates an RSA key pair from your password, and encrypts all important stuff and stores them in a file, which can be decrypted using the same password! anyone can verify from looking at the script :3

## Contact me

- If you find any bugs/exploits ... plz inform
- New features?
  - Inform me .... ill do it if i like it else hell nah .... fork this script and do it yourself
