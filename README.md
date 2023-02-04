
# Password Manger

Personal project, aimed to build a fully functional Password Manager. Including a Vault, that encrypts all information 
using PBKDF2_HMAC to run each salted password through sha256 100,000 times. A generator that will create passwords, 
passphrase, email sub-addresses, and username. A password strength checker with a custom algorithm that uses more than 
just the length of the password to determine strength.

### Disclaimer
I do not recommend using this to store your passwords. It is littered with many security flaws, such as secure notes 
and password history, storing the encryption key in the database.  It only exists as a personal project to aid in 
understanding and implementing password security.