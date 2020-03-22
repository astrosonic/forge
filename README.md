# forge
Forensics Oriented Reporting Group Under Encryption


## Ideology
**This project is follows the belief of Sir Abraham Lincoln**
> You can fool *all* the people *some* of the time and *some* of the people *all* the time,
> But you cannot fool *all* the people *all* the time.

## Introduction
FORGE or Forensics Oriented Reporting Group Under Encryption is a network system for secure transmission of directives among two or multiple authentic users. It uses asymmetric key cryptography to ensure an end-to-end encryption scenario.

## Features
* Directives are stored in eavesdrop-free encrypted format in the server
* Every user has a unique 64-byte PKCS identity to recognize with
* Encryption uses a brute-force resistant timestamp based keypair generation
* Asymmetric key cryptography - 2048-bit RSA used for directive protection
* One-way encryption strategy - 512-bit SHA used for storing passwords
* Group sharing uses double layer protection with group's own keypair 
* Capable of one-to-one directive sharing using *composition*
* Capable of one-to-many directive sharing using *broadcast* and *groups*
* State-of-the-art session management and user access control

## Changelog
**NOTE** : Project follows a rolling version control model  

### v17032020
* Built basic flow-of-control framework
* Elected UIKit CSS framework for look-and-feel
* Elected SQLite3 database for testing purposes
* Elected SHA512 as the default hashing method
* Designed `localuse` database schema (one-for-one)
* Designed `clouduse` database schema (one-for-many)
* Built login backbone
  * Added validation check for existing account
  * Enabled storing passwords as 512-bit SHA hash
  * Added login check by hash comparison
  * Created frontend for login page

### v18032020
* Elected RSA2048 as the default asymmetric encryption method
* Built signup backbone
  * Added validation check for existing account
  * Enabled storing passwords as 512-bit SHA hash
  * Enabled timestamp-based keypair generation
  * Enabled storing public key in `clouduse` remote database
  * Enabled storing private key in `localuse` local database
  * Added a 64-byte PKCS identity for user
  * Created frontend for signup page
  * Created frontend for login redirect
* Built dashboard backbone
  * Created frontend for dashboard page
  * Added link to compose page
  * Added link to inbox page
  * Added link to contacts page
  * Added link to trashcan page
  * Added link to broadcast page
  * Added link to settings page
  * Added link to logout

### v19032020
* Updated login backbone
  * Added validation check for empty username response
  * Added validation check for empty password response
* Updated signup backbone
  * Added validation check for empty username response
  * Added validation check for empty password response
  * Added validation check for empty email address
  * Added validation check for invalid email address
  * Added validation check for dissimilar passwords
* Built configuration system
  * Added `localuse` database credentials
  * Added `clouduse` database credentials
  * Added timekeeping metadata
  * Added centralized version info
  * Added centralized error handling routine

### v20032020
* Built compose backbone
  * Enable one-to-one directive sharing
  * Added validation check for existing account
  * Added receiver public key fetch function - sending
  * Added sender public key fetch function - saving
  * Enabled *subject* encryption for sending and saving
  * Enabled *content* encryption for sending and saving
  * Added timestamp-based 64-byte mail identity
  * Enable storage in byte-index array
  * Disabled remove flag by default for all directives
