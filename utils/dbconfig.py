import psycopg2

from rich import print as printc
from rich.console import Console
console = Console()

def dbconfig(database="pm"):
    try:
        db = psycopg2.connect(
            host='localhost',
            user='pm',
            password='password',
            dbname=database
        )

    except Exception as e:
        console.print_exception(show_locals=True)

    return db
