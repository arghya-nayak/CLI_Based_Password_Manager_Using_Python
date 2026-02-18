import sys
import random
import string
import hashlib
from getpass import getpass

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from utils.dbconfig import dbconfig

from rich import print as printc
from rich.console import Console
console = Console()

def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def config():
    # Connect to the default 'postgres' database to create our database
    try:
        db = psycopg2.connect(
            host='localhost',
            user='pm',
            password='password',
            dbname='postgres'
        )
        db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE pm")
        db.close()
    except Exception as e:
        printc("[red][!] An error occurred while trying to create the db.[/red]")
        console.print_exception(show_locals=True)
        sys.exit(0)
    printc("[green][+][/green] Database 'pm' created")

    # Connect to the new 'pm' database to create tables
    db = dbconfig(database="pm")
    cursor = db.cursor()

    # In PostgreSQL we use the public schema (no "pm." prefix needed)
    query = """
        CREATE TABLE secrets (
            masterkey_hash TEXT NOT NULL,
            device_secret TEXT NOT NULL
        )
    """
    cursor.execute(query)
    printc("[green][+][/green] Table 'secrets' created")

    query = """
        CREATE TABLE entries (
            sitename TEXT NOT NULL,
            siteurl TEXT NOT NULL,
            email TEXT,
            username TEXT,
            password TEXT NOT NULL
        )
    """
    cursor.execute(query)
    printc("[green][+][/green] Table 'entries' created")

    while True:
        mp = getpass("Choose a MASTER PASSWORD : ")
        if mp == getpass("Re-Type: ") and mp != "":
            break
        printc("[yellow][-] Please try again.[/yellow]")

    # Hash the MASTER PASSWORD
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc("[green][+][/green] Generated hash of MASTER PASSWORD")

    # Generate a DEVICE SECRET
    ds = generateDeviceSecret()
    printc("[green][+][/green] Device Secret Generated")

    # Add to the DB
    query = "INSERT INTO secrets (masterkey_hash, device_secret) VALUES (%s, %s)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+][/green] Added to the database")
    printc("[green][+] Configuration done![/green]")

    db.close()

config()
