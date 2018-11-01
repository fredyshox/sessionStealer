# Session Stealer

Script for stealing unecrypted web sessions.

## Usage
Required parameters
- path to \*.pcapng input file which contains sniffed http conversation
- name of cookie used for session id
- hostname
```
$ python3 sessionSteal.py -H host.name -c cookie.name -i example.pcapng
```
