from utils.dbconfig import dbconfig
import utils.aesutil
from getpass import getpass

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64

from rich import print as printc
from rich.console import Console

def computeMasterKey(mp, ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


def checkEntry(sitename, siteurl, email, username):
    db = dbconfig()
    cursor = db.cursor()
    query = "SELECT * FROM entries WHERE sitename = %s AND siteurl = %s AND email = %s AND username = %s"
    cursor.execute(query, (sitename, siteurl, email, username))
    results = cursor.fetchall()
    db.close()

    if len(results) != 0:
        return True
    return False


def addEntry(mp, ds, sitename, siteurl, email, username):
    # Check if the entry already exists
    if checkEntry(sitename, siteurl, email, username):
        printc("[yellow][-][/yellow] Entry with these details already exists")
        return

    # Input Password
    password = getpass("Password: ")

    # Compute master key
    mk = computeMasterKey(mp, ds)

    # Encrypt password with mk
    encrypted = utils.aesutil.encrypt(key=mk, source=password, keyType="bytes")

    # Add to db
    db = dbconfig()
    cursor = db.cursor()
    query = "INSERT INTO entries (sitename, siteurl, email, username, password) VALUES (%s, %s, %s, %s, %s)"
    val = (sitename, siteurl, email, username, encrypted)
    cursor.execute(query, val)
    db.commit()
    db.close()

    printc("[green][+][/green] Added entry")
