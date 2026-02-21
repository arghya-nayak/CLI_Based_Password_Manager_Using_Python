from utils.dbconfig import dbconfig
from rich import print as printc
from rich.console import Console
from rich.table import Table

console = Console()


def listEntries():
    """List all entries with their IDs"""
    db = dbconfig()
    cursor = db.cursor()
    query = "SELECT ctid, sitename, siteurl, email, username FROM entries"
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    
    if len(results) == 0:
        printc("[yellow][-][/yellow] No entries found in the database")
        return []
    
    table = Table(title="All Entries")
    table.add_column("ID", style="cyan", width=8)
    table.add_column("Site Name", style="green", width=20)
    table.add_column("URL", style="blue", width=30)
    table.add_column("Email", style="yellow", width=25)
    table.add_column("Username", style="magenta", width=20)
    
    for idx, entry in enumerate(results, 1):
        table.add_row(
            str(idx),
            entry[1] or "",
            entry[2] or "",
            entry[3] or "",
            entry[4] or ""
        )
    
    console.print(table)
    return results


def deleteEntry(sitename, siteurl, email, username):
    """Delete a specific entry"""
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
    
    # Delete the entry
    query = "DELETE FROM entries WHERE sitename = %s AND siteurl = %s AND email = %s AND username = %s"
    cursor.execute(query, (sitename, siteurl, email, username))
    db.commit()
    db.close()
    
    printc("[green][+][/green] Entry deleted successfully")
    return True


def deleteEntryById(entry_id, all_entries):
    """Delete entry by ID from the list"""
    if entry_id < 1 or entry_id > len(all_entries):
        printc("[red][!][/red] Invalid ID")
        return False
    
    entry = all_entries[entry_id - 1]
    sitename = entry[1]
    siteurl = entry[2]
    email = entry[3]
    username = entry[4]
    
    return deleteEntry(sitename, siteurl, email, username)
