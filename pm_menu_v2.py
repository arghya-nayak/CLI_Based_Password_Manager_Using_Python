import hashlib
from getpass import getpass
import pyperclip

from rich import print as printc
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich import box

import utils.add
import utils.retrieve
import utils.generate
import utils.delete
import utils.update
from utils.dbconfig import dbconfig

console = Console()


def clear_screen():
    """Clear the console screen"""
    console.clear()


def show_banner():
    """Display a beautiful banner"""
    banner_panel = Panel(
        Align.center(
            Text.from_markup(
                "[bold yellow]🔐 PASSWORD MANAGER 🔐[/bold yellow]\n\n"
                "[bold green]Secure • Encrypted • PostgreSQL[/bold green]"
            )
        ),
        border_style="cyan",
        padding=(1, 2),
        width=60
    )
    
    console.print(Align.center(banner_panel))
    console.print()


def show_menu():
    """Display the main menu with beautiful formatting"""
    clear_screen()
    show_banner()
    
    menu_panel = Panel(
        """
[bold yellow]1.[/bold yellow] Add New Password Entry
[bold yellow]2.[/bold yellow] View All Entries
[bold yellow]3.[/bold yellow] Search & Extract Password
[bold yellow]4.[/bold yellow] Delete Entry
[bold yellow]5.[/bold yellow] Generate Random Password
[bold yellow]6.[/bold yellow] Exit
        """,
        title="[bold magenta]Main Menu[/bold magenta]",
        border_style="bright_blue",
        padding=(1, 4)
    )
    
    console.print(menu_panel)
    console.print()


def validate_master_password():
    """Validate master password and return credentials"""
    console.print(Panel(
        "[yellow]🔑 Authentication Required[/yellow]",
        border_style="yellow",
        padding=(0, 2)
    ))
    
    mp = getpass("Enter MASTER PASSWORD: ")
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

    try:
        db = dbconfig()
        cursor = db.cursor()
        query = "SELECT * FROM secrets"
        cursor.execute(query)
        result = cursor.fetchall()[0]
        db.close()

        if hashed_mp != result[0]:
            console.print("\n[bold red]❌ WRONG PASSWORD![/bold red]\n")
            return None

        console.print("\n[bold green]✅ Authentication successful![/bold green]\n")
        return [mp, result[1]]
    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/bold red]\n")
        return None


def add_entry():
    """Add a new password entry"""
    clear_screen()
    console.print(Panel(
        "[bold cyan]➕ ADD NEW PASSWORD ENTRY[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()
    
    res = validate_master_password()
    if res is None:
        input("\nPress Enter to continue...")
        return

    console.print(Panel(
        "[yellow]Please enter the following details:[/yellow]",
        border_style="yellow",
        padding=(0, 2)
    ))
    console.print()
    
    sitename = Prompt.ask("🌐 [bold green]Site Name[/bold green]")
    siteurl = Prompt.ask("🔗 [bold green]Site URL[/bold green]")
    email = Prompt.ask("📧 [bold green]Email[/bold green] [dim](optional)[/dim]", default="")
    username = Prompt.ask("👤 [bold green]Username[/bold green]")

    console.print()
    utils.add.addEntry(res[0], res[1], sitename, siteurl, email, username)
    
    console.print()
    input("Press Enter to continue...")


def view_all_entries():
    """View all password entries"""
    clear_screen()
    console.print(Panel(
        "[bold cyan]📋 ALL PASSWORD ENTRIES[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()
    
    res = validate_master_password()
    if res is None:
        input("\nPress Enter to continue...")
        return

    # Get entries from database
    try:
        db = dbconfig()
        cursor = db.cursor()
        query = "SELECT * FROM entries"
        cursor.execute(query)
        results = cursor.fetchall()
        db.close()

        if len(results) == 0:
            console.print(Panel(
                "[yellow]No entries found in the database.[/yellow]",
                border_style="yellow",
                padding=(1, 2)
            ))
        else:
            table = Table(
                title=f"[bold magenta]Total Entries: {len(results)}[/bold magenta]",
                box=box.ROUNDED,
                border_style="green",
                show_lines=True
            )
            table.add_column("🌐 Site Name", style="cyan", width=20)
            table.add_column("🔗 URL", style="blue", width=30)
            table.add_column("📧 Email", style="yellow", width=25)
            table.add_column("👤 Username", style="green", width=20)
            table.add_column("🔒 Password", style="red", width=12)

            for entry in results:
                table.add_row(
                    entry[0] or "",
                    entry[1] or "",
                    entry[2] or "",
                    entry[3] or "",
                    "••••••••"
                )
            
            console.print(table)
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
    
    console.print()
    input("Press Enter to continue...")


def search_and_extract():
    """Search for entries and optionally extract password"""
    clear_screen()
    console.print(Panel(
        "[bold cyan]🔍 SEARCH & EXTRACT PASSWORD[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()
    
    res = validate_master_password()
    if res is None:
        input("\nPress Enter to continue...")
        return

    console.print(Panel(
        "[yellow]Enter search criteria (leave blank to skip):[/yellow]",
        border_style="yellow",
        padding=(0, 2)
    ))
    console.print()
    
    search = {}
    
    sitename = Prompt.ask("🌐 [bold green]Site Name[/bold green]", default="")
    if sitename:
        search["sitename"] = sitename
    
    siteurl = Prompt.ask("🔗 [bold green]Site URL[/bold green]", default="")
    if siteurl:
        search["siteurl"] = siteurl
    
    email = Prompt.ask("📧 [bold green]Email[/bold green]", default="")
    if email:
        search["email"] = email
    
    username = Prompt.ask("👤 [bold green]Username[/bold green]", default="")
    if username:
        search["username"] = username

    if not search:
        console.print("\n[yellow]ℹ️  No search criteria provided. Showing all entries...[/yellow]\n")
    
    copy_password = Confirm.ask(
        "\n[bold cyan]📋 Copy password to clipboard?[/bold cyan]",
        default=False
    )
    
    console.print()
    utils.retrieve.retrieveEntries(
        res[0], 
        res[1], 
        search, 
        decryptPassword=copy_password
    )
    
    console.print()
    input("Press Enter to continue...")


def generate_password():
    """Generate a random password"""
    clear_screen()
    console.print(Panel(
        "[bold cyan]🎲 GENERATE RANDOM PASSWORD[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()
    
    length = IntPrompt.ask(
        "🔢 [bold green]Enter password length[/bold green]"
    )
    
    password = utils.generate.generatePassword(length)
    pyperclip.copy(password)
    
    # Display password in a nice centered box
    console.print()
    password_panel = Panel(
        Align.center(Text(password, style="bold yellow")),
        title="[bold green]Generated Password[/bold green]",
        border_style="green",
        padding=(1, 2),
        width=60
    )
    console.print(Align.center(password_panel))
    console.print()
    
    console.print(Panel(
        "[bold green]✅ Password generated successfully!\n📋 Password copied to clipboard![/bold green]",
        border_style="green",
        padding=(1, 2)
    ))
    
    console.print()
    input("Press Enter to continue...")


def update_entry():
    """Update an existing password entry"""
    clear_screen()
    console.print(Panel(
        "[bold cyan]✏️ UPDATE PASSWORD[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()
    
    res = validate_master_password()
    if res is None:
        input("\nPress Enter to continue...")
        return

    console.print(Panel(
        "[yellow]Enter details of the entry to update:[/yellow]",
        border_style="yellow",
        padding=(0, 2)
    ))
    console.print()
    
    sitename = Prompt.ask("🌐 [bold green]Site Name[/bold green]")
    siteurl = Prompt.ask("🔗 [bold green]Site URL[/bold green]")
    email = Prompt.ask("📧 [bold green]Email[/bold green] [dim](optional)[/dim]", default="")
    username = Prompt.ask("👤 [bold green]Username[/bold green] [dim](optional)[/dim]", default="")

    console.print()
    utils.update.updateEntry(res[0], res[1], sitename, siteurl, email, username)
    
    console.print()
    input("Press Enter to continue...")


def delete_entry():
    """Delete a password entry"""
    clear_screen()
    console.print(Panel(
        "[bold cyan]DELETE ENTRY[/bold cyan]",
        border_style="cyan",
        padding=(0, 2),
        width=45
    ))
    console.print()
    
    # Require master password authentication first
    res = validate_master_password()
    if res is None:
        input("\nPress Enter to continue...")
        return
    
    # Show all entries
    console.print(Panel(
        "[yellow]All saved entries:[/yellow]",
        border_style="yellow",
        padding=(0, 2),
        width=45
    ))
    console.print()
    
    all_entries = utils.delete.listEntries()
    
    if len(all_entries) == 0:
        input("\nPress Enter to continue...")
        return
    
    console.print()
    
    try:
        entry_id = IntPrompt.ask(
            "🔢 [bold green]Enter the ID of the entry to delete[/bold green] [dim](0 to cancel)[/dim]"
        )
        
        if entry_id == 0:
            console.print("\n[yellow][-][/yellow] Cancelled")
            input("\nPress Enter to continue...")
            return
        
        confirm = Confirm.ask(
            f"\n[bold red]⚠️  Are you sure you want to delete entry {entry_id}?[/bold red]",
            default=False
        )
        
        if confirm:
            utils.delete.deleteEntryById(entry_id, all_entries)
        else:
            console.print("\n[yellow][-][/yellow] Cancelled")
    except ValueError:
        console.print("\n[red][!][/red] Invalid input")
    
    console.print()
    input("Press Enter to continue...")


def main():
    """Main menu loop"""
    while True:
        show_menu()
        
        choice = Prompt.ask(
            "[bold cyan]Select an option[/bold cyan]",
            choices=["1", "2", "3", "4", "5", "6"]
        )
        
        if choice == "1":
            add_entry()
        elif choice == "2":
            view_all_entries()
        elif choice == "3":
            search_and_extract()
        elif choice == "4":
            delete_entry()
        elif choice == "5":
            generate_password()
        elif choice == "6":
            clear_screen()
            console.print()
            console.print(Panel(
                "[bold green]✨ Thank you for using Password Manager! ✨\n🔒 Your passwords are safe and secure! 🔒[/bold green]",
                border_style="green",
                padding=(1, 2)
            ))
            console.print()
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        console.print()
        console.print(Panel(
            "[bold yellow]⚠️  Exited by user[/bold yellow]",
            border_style="yellow",
            padding=(1, 2)
        ))
        console.print()
    except Exception as e:
        console.print()
        console.print(Panel(
            f"[bold red]❌ An error occurred:[/bold red]\n{e}",
            border_style="red",
            padding=(1, 2)
        ))
        console.print_exception(show_locals=True)
        console.print()