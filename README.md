# forge
Forensics Oriented Reporting Group Under Encryption

## Ideology
**This project follows the belief of Sir Abraham Lincoln**
> You can fool *all* the people *some* of the time and *some* of the people *all* the time,  
> But you cannot fool *all* the people *all* the time.

## Introduction
FORGE or Forensics Oriented Reporting Group Under Encryption is a network system for secure transmission of directives among two or multiple authentic users. It uses asymmetric key cryptography to ensure an end-to-end encryption scenario.

## Features
* Can be easily adopted in any network using client-server model
* Directives are stored in eavesdrop-free encrypted format in the server
* Every user has a unique **64-byte PKCS identity** to recognize with
* Encryption uses a brute-force resistant *timestamp-based keypair generation*
* Directive subject and content storage in tamper-free *byte-index array*
* Asymmetric key cryptography - **2048-bit RSA** used for *directive protection*
* One-way encryption strategy - **512-bit SHA** used for *storing passwords*
* Unique signature for elements like contacts, directives and groups
* Group sharing uses double layer protection with group's own keypair
* Capable of **one-to-one directive sharing** using *composition*
* Capable of **one-to-many directive sharing** using *broadcast* and *groups*
* State-of-the-art session management and user access control

## Usage

### Server-side instructions
1.  Install and upgrade **virtualenv** if not already done by executing ```pip3 install virtualenv --user```
2.  Clone the repository on your local drive and make it your current working directory
3.  Create a virtual environment by executing ```virtualenv venv```
4.  Activate the virtual environment by executing ```source venv/bin/activate```
5.  Install all dependencies for the project by executing ```pip3 install -r requirements.txt```
6.  Run the project server by executing ```python3 app.py```
7.  When done tinkering, deactivate the virtual environment by executing ```deactivate```
8.  Give stars to the repository if it was helpful

### Client-side instructions
1. Open up a browser and visit ```<SERVER-IP-ADDRESS>:6969``` (default location)
2. Create account, login, follow people and send protected directives
3. Safely logout of your account once you are done using it
4. Give stars to the repository if it was helpful

## Changelog
[You can find all changes listed here](https://github.com/t0xic0der/forge/blob/master/CHANGELOG.md)

## Screenshots
[You can find all shiny stuff here](https://github.com/t0xic0der/forge/blob/master/SCREENSHOTS.md)

## Contribute
The project is currently in diverse development process. The codebase needs cleanup, optimization and documentation so one may find it hard to get their hands into it. Feel free to contact me at akashdeep.dhar@gmail.com if you wish to contribute.
