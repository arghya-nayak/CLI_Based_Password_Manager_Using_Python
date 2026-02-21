from utils.dbconfig import dbconfig
import utils.aesutil
from getpass import getpass

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512

from rich import print as printc


def computeMasterKey(mp, ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


def updateEntry(mp, ds, sitename, siteurl, email, username, new_password=None):
    """Update an existing entry's password"""
    db = dbconfig()
    cursor = db.cursor()
    
    # Check if entry exists
    query = "SELECT * FROM entries WHERE sitename = %s AND siteurl = %s AND email = %s AND username = %s"
    cursor.execute(query, (sitename, siteurl, email, username))
    result = cursor.fetchone()
    
    if not result:
        printc("[yellow][-][/yellow] Entry not found")
        db.close()
        return False
    
    # Get new password if not provided
    if new_password is None:
        new_password = getpass("Enter new password: ")
    
    # Compute master key
    mk = computeMasterKey(mp, ds)
    
    # Encrypt new password
    encrypted = utils.aesutil.encrypt(key=mk, source=new_password, keyType="bytes")
    
    # Update in database
    query = "UPDATE entries SET password = %s WHERE sitename = %s AND siteurl = %s AND email = %s AND username = %s"
    cursor.execute(query, (encrypted, sitename, siteurl, email, username))
    db.commit()
    db.close()
    
    printc("[green][+][/green] Password updated successfully")
    return True
