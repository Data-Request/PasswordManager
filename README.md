# Password Manager

Personal project, aimed to build a fully functional Password Manager that stores data in a database using 
[sqlite3](https://docs.python.org/3/library/sqlite3.html), and 
[CustomerTkinter](https://github.com/TomSchimansky/CustomTkinter/blob/master/Readme.md) to create a modern UI.

---

## Features

<p align="center">
  <picture>
    <img src="/documentation_images/features.jpg">
  </picture>
</p>

When an account is created, a random salt is generated using [os.urandom](https://docs.python.org/3/library/os.html#os.urandom) 
and added to your master password. This is run through Password-Based Key Derivation Function 2 (PBKDF2) with a default 
of 480,000 iterations to create a Master Key. From this Master Key, your Master Password is attached and ran through 
PBKDF2 again to create a Master Password Hash, this hash is stored in the database and used to verify a sign-in attempt.

---

### Vault
Users can create secure notes, and create logins that can be stored within user created folders. Both types of vault 
data is encrypted with symmetric authenticated cryptography using a key derived from your Master Key. The only data 
stored in plaintext is the name of the folder in which each login is stored.

---

### Password Generator
The built-in password generator will create passwords, passphrase, usernames, and email sub-addresses. Various 
settings, such as length, minimum number of symbols, or the ability to avoid using ambiguous characters, can be 
changed to create a password that suits your needs. A real-time password strength meter shows the strength of your
currently generated password.

---

### Password Strength Checker
While the consensus is that a longer password is always going to be better, real-world scenarios doesn't allow this 
to be the case. Hackers today rarely rely on brute force alone to get a password, dictionary attacks, rainbow table
attacks, and many other forms, force us to use more sophisticated password. While no official password grading system 
exists, The Password Strength Checker is based on the work of [The Password Meter](http://www.passwordmeter.com/), 
which uses custom formulas to assess the strength of a password.

---

### Disclaimer

I do not recommend using this to store your passwords. It only exists as a personal project to aid in my understanding 
and implementing password security, and database management, and source control using Git. There are many better made
and documented open source password managers available for uses, such as [Passbolt](https://www.passbolt.com/), 
[Bitwarden](https://bitwarden.com/), [Keepass](https://keepass.info/), [Padloc](https://padloc.app/)
