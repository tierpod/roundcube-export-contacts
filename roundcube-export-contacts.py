#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Export roundcube contacts in vcard format from mysql database.
"""

import argparse
import codecs
import json
import mysql.connector
import os
import os.path
from collections import namedtuple


DEFAULT_CONFIG = "./config.json"
DEFAULT_OUT = "./out"


# structures
User = namedtuple("User", ["id", "email"])
Contact = namedtuple("Contact", ["email", "vcard", "words", "deleted"])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="json config", default=DEFAULT_CONFIG)
    parser.add_argument("--out", help="output directory path", default=DEFAULT_OUT)
    return parser.parse_args()


def load_config(path):
    with open(path, "r") as fobj:
        config = json.load(fobj)
    return config


def get_users(mysql_cnx):
    """Get all 'user_id' and 'username' from 'users' table.

    Args:
        mysql_cnx: connection to mysql database

    Returns:
        mysql_users: sql query result
    """

    mysql_cur = mysql_cnx.cursor()
    query = ("SELECT user_id, username FROM users")

    mysql_cur.execute(query)
    mysql_users = mysql_cur.fetchall()

    return mysql_users


def get_contacts(mysql_cnx, user):
    """Get 'email', 'vcard', 'words' and 'del' from contacts table.

    Args:
        mysql_cnx: connection to mysql database
        user: User namedtuple

    Returns:
        mysql_contacts: sql query result
    """

    mysql_cur = mysql_cnx.cursor()

    query = ("SELECT email, vcard, words, del FROM contacts WHERE user_id = %s")
    data = (user.id, )

    mysql_cur.execute(query, data)
    mysql_contacts = mysql_cur.fetchall()

    return mysql_contacts


def save_vcard(out, vcard):
    """Save `vcard` data to `out` file.

    Args:
        out: output file
        vcard: vcard data
    """

    if os.path.exists(out):
        print("Append to file %s" % out)
    else:
        print("Create file: %s" % out)

    with codecs.open(out, "a", "utf-8") as fobj:
        fobj.write(vcard)
        fobj.write("\n")


def main():
    args = parse_args()
    config = load_config(args.config)

    if not os.path.exists(args.out):
        os.mkdir(args.out)

    # connect to databases
    mysql_cnx = mysql.connector.connect(buffered=True, **config["mysql"])

    users = get_users(mysql_cnx)
    for user in users:
        user = User(user[0], user[1])
        contacts = get_contacts(mysql_cnx, user)
        for contact in contacts:
            contact = Contact(contact[0], contact[1], contact[2], contact[3])
            filename = "%s_%s%s.vcf" % (user.email, user.id, "_deleted" if contact.deleted else "")
            out = os.path.join(args.out, filename)
            save_vcard(out, contact.vcard)

    mysql_cnx.close()


if __name__ == "__main__":
    main()
