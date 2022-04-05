roundcube-export-contacts
=========================

Export roundcube contacts in vcard format from mysql database.

Saves all exported data from "contacts" table, "vcard" column to files like
'./out/{EMAIL}_{USERID}.vcf'

For example:

```bash
./out/myemail@localhost_1.vcf  # active vcards
./out/myemail@localhost_1_deleted.vcf  # deleted vcards
```

where:
* myemail@localhost - data from 'users.username'
* 1 - data from 'users.user_id'
* deleted - deleted vcards (contacts.del = 1)

Installation
------------

Using virtual env:

```bash
# create venv
make venv
# enable venv
source ./venv/bin/activate
# install requirements
make init
# run
./roundcube-export-contacts.py -h
```
