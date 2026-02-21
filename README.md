# CLI Based Password Manager Using Python
# 🔐 Secure Password Manager

A robust, locally-stored password manager built with Python and PostgreSQL, featuring military-grade AES-256 encryption to keep your passwords safe and secure.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![PostgreSQL](https://img.shields.io/badge/postgresql-17-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

---

## 📋 Table of Contents

- [Features](#-features)
- [Security](#-security)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Migration from MariaDB](#-migration-from-mariadb)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

- 🔒 **Military-Grade Encryption**: AES-256 encryption for all stored passwords
- 🔑 **Master Password Protection**: Single password to access all your credentials
- 🎲 **Password Generator**: Create strong, random passwords instantly
- 🔍 **Quick Search**: Find passwords by site name, URL, email, or username
- 🗑️ **Secure Deletion**: Master password required to delete entries
- 💻 **Two Interfaces**: 
  - Command-line interface (CLI) for quick operations
  - Interactive menu with beautiful formatting
- 📦 **Local Storage**: Your data stays on your computer, not in the cloud
- 🚀 **PostgreSQL Backend**: Fast, reliable, and scalable database
- 🎨 **Beautiful UI**: Rich console formatting with colors and panels

---

## 🛡️ Security

Your security is our top priority. This password manager implements multiple layers of protection:

### Security Layers

1. **SHA-256 Hashing**
   - Master password is hashed using SHA-256
   - One-way function: cannot be reversed
   - Hash is stored, not the actual password

2. **Device Secret**
   - Random 10-character secret generated during setup
   - Unique to your installation
   - Acts as a salt for key derivation

3. **PBKDF2 Key Derivation**
   - Combines master password + device secret
   - 1,000,000 iterations with SHA-512
   - Makes brute-force attacks computationally expensive
   - Generates a 256-bit encryption key

4. **AES-256 Encryption**
   - Industry-standard encryption algorithm
   - Same encryption used by governments and banks
   - Each password encrypted individually
   - Random Initialization Vector (IV) for each encryption

5. **SQL Injection Protection**
   - All queries use parameterized statements
   - User input is never directly concatenated into SQL
   - Prevents database manipulation attacks

### Why These Methods?

- **SHA-256**: Industry standard, cryptographically secure hash function
- **PBKDF2**: Recommended by NIST, used in WPA2, SSL/TLS
- **AES-256**: Military-grade, never been cracked, trusted worldwide
- **1M Iterations**: Slows down attackers from ~1B passwords/sec to ~2/sec

---

## 🛠️ Technology Stack

### Core Technologies

- **Python 3.8+**: Primary programming language
- **PostgreSQL 17**: Robust, scalable database system

### Python Libraries

- `psycopg2-binary`: PostgreSQL database adapter
- `pycryptodome`: Cryptographic library (AES, SHA, PBKDF2)
- `rich`: Beautiful terminal formatting and UI
- `pyperclip`: Clipboard operations
- `argparse`: Command-line argument parsing

### Why PostgreSQL?

We migrated from MariaDB to PostgreSQL for several reasons:

✅ **Better Performance**: Handles complex queries more efficiently  
✅ **Industry Standard**: Used by Instagram, Spotify, Reddit  
✅ **Advanced Features**: JSON support, full-text search, CTEs  
✅ **Scalability**: Can handle millions of entries  
✅ **Reliability**: Superior ACID compliance and data integrity  

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 17 or higher

### Step 1: Install PostgreSQL

#### Windows
1. Download from [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)
2. Run the installer
3. Remember the password you set for `postgres` user
4. Keep default port (5432)

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### macOS
```bash
brew install postgresql@17
```

### Step 2: Create Database User

#### Windows (PowerShell)
```powershell
psql -U postgres
```

#### Linux
```bash
sudo -u postgres psql
```

Then in the PostgreSQL prompt:
```sql
CREATE USER pm WITH PASSWORD 'password';
ALTER USER pm CREATEDB;
\q
```

**Note**: Change `'password'` to a secure password and update `utils/dbconfig.py` accordingly.

### Step 3: Install Python Dependencies

```bash
pip install psycopg2-binary pycryptodome rich pyperclip
```

### Step 4: Clone the Repository

```bash
git clone https://github.com/arghya-nayak/CLI_Based_Password_Manager_Using_Python.git
cd CLI_Based_Password_Manager_Using_Python
```

### Step 5: Run Configuration

```bash
python config.py
```

This will:
- Create the `pm` database
- Create necessary tables (`secrets` and `entries`)
- Prompt you to set your master password
- Generate a unique device secret

**⚠️ Important**: Choose a strong master password and remember it! If you forget it, you cannot recover your passwords.

---

## 🚀 Usage

### Interactive Menu (Recommended)

For a user-friendly experience with guided prompts:

```bash
python pm_menu_v2.py
```

**Menu Options:**
1. Add New Password Entry
2. View All Entries
3. Search & Extract Password
4. Delete Entry
5. Generate Random Password
6. Exit

> **Note**: Use `pm_menu_v2.py` (version 2) which includes the delete feature with master password protection. The original `pm_menu.py` is a legacy version without delete functionality.

### Command-Line Interface

For quick operations via terminal:

#### Add a Password
```bash
python pm.py a -s "GitHub" -u "https://github.com" -l "username" -e "email@example.com"
```

#### View All Passwords
```bash
python pm.py e
```

#### Search and Copy Password
```bash
python pm.py e -s "GitHub" -c
```

#### Generate Random Password
```bash
python pm.py g --length 16
```

#### Delete an Entry
```bash
python pm.py d
```

### Command-Line Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `a` / `add` | Add new password entry | ✅ |
| `e` / `extract` | View/search entries | ✅ |
| `g` / `generate` | Generate random password | ✅ |
| `d` / `delete` | Delete an entry | ✅ |
| `-s` / `--name` | Site name | For add/search |
| `-u` / `--url` | Site URL | For add |
| `-l` / `--login` | Username | For add |
| `-e` / `--email` | Email address | Optional |
| `--length` | Password length | For generate |
| `-c` / `--copy` | Copy password to clipboard | Optional |

---

## 📁 Project Structure

```
password-manager/
│
├── config.py                 # Initial setup and configuration
├── pm.py                     # Command-line interface
├── pm_menu.py               # Interactive menu (basic version)
├── pm_menu_v2.py            # Interactive menu v2 (with delete feature)
│
├── utils/
│   ├── dbconfig.py          # Database connection handler
│   ├── add.py               # Add password functionality
│   ├── retrieve.py          # Search and retrieve passwords
│   ├── delete.py            # Delete password entries
│   ├── generate.py          # Random password generator
│   └── aesutil.py           # Encryption/decryption utilities
│
├── .gitignore               # Git ignore file
├── LICENSE                  # MIT License
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

### File Descriptions

- **config.py**: Run once during initial setup. Creates database, tables, and stores your hashed master password.
- **pm.py**: Command-line interface for quick password operations.
- **pm_menu.py**: Basic interactive menu (legacy version without delete feature).
- **pm_menu_v2.py**: **Current version** - Interactive menu with all features including delete functionality.
- **dbconfig.py**: Handles PostgreSQL connections with error handling.
- **add.py**: Encrypts and stores new password entries.
- **retrieve.py**: Searches database and decrypts passwords.
- **delete.py**: Securely removes password entries with master password verification.
- **generate.py**: Creates strong random passwords.
- **aesutil.py**: Core encryption/decryption using AES-256-CBC.

### Which File to Use?

**Use `pm_menu_v2.py`** for the interactive menu - it includes all features:
- Add passwords
- View all entries
- Search & extract passwords
- **Delete entries** (with master password protection)
- Generate random passwords
- Exit

The original `pm_menu.py` is kept for reference but `pm_menu_v2.py` is the recommended version.

---

## 🔍 How It Works

### Adding a Password

1. **Authenticate**: Enter your master password
2. **Verify**: Program hashes your input and compares with stored hash
3. **Derive Key**: Combines master password + device secret using PBKDF2 (1M iterations)
4. **Encrypt**: Your password is encrypted with AES-256-CBC
5. **Store**: Encrypted password saved to PostgreSQL database

```
Your Password → AES-256 Encryption → Database
                     ↑
                     |
            PBKDF2 Derived Key
                     ↑
                     |
        Master Password + Device Secret
```

### Retrieving a Password

1. **Authenticate**: Enter your master password
2. **Search**: Query database for matching entries
3. **Derive Key**: Regenerate encryption key using PBKDF2
4. **Decrypt**: Encrypted password is decrypted with AES-256-CBC
5. **Copy**: Decrypted password copied to clipboard

### Encryption Details

```python
# Key Derivation
key = PBKDF2(
    password=master_password,
    salt=device_secret,
    dkLen=32,              # 256 bits
    count=1000000,         # 1 million iterations
    hmac_hash_module=SHA512
)

# Encryption
IV = random(16 bytes)      # Random initialization vector
cipher = AES.new(key, AES.MODE_CBC, IV)
encrypted = IV + cipher.encrypt(padded_password)
stored = base64.encode(encrypted)
```

---

## 🐘 Why PostgreSQL?

PostgreSQL was chosen as the database system for this password manager for several compelling reasons:

### Performance & Reliability

- **ACID Compliance**: PostgreSQL provides full ACID (Atomicity, Consistency, Isolation, Durability) guarantees, ensuring your password data is never corrupted or lost
- **Efficient Indexing**: Advanced indexing capabilities make password searches lightning-fast, even with thousands of entries
- **Connection Pooling**: Handles multiple connections efficiently without performance degradation
- **Write-Ahead Logging**: Ensures data integrity even in case of system crashes

### Security Features

- **Row-Level Security**: Can implement fine-grained access controls if needed
- **SSL Connections**: Supports encrypted connections between application and database
- **Data Encryption**: Native support for encrypted columns and connections
- **Audit Logging**: Comprehensive logging capabilities for security monitoring

### Advanced Capabilities

- **JSON Support**: Store and query complex data structures if needed
- **Full-Text Search**: Built-in support for searching through encrypted metadata
- **CTEs (Common Table Expressions)**: Write cleaner, more maintainable queries
- **Window Functions**: Analyze password usage patterns and security metrics

### Industry Adoption

- **Battle-Tested**: Used by major companies like Instagram, Spotify, Reddit, Uber
- **Open Source**: Free, community-driven, no vendor lock-in
- **Active Development**: Regular updates with new features and security patches
- **Extensive Documentation**: Comprehensive guides and strong community support

### Scalability

- **Handles Large Datasets**: Can efficiently manage millions of password entries
- **Horizontal Scaling**: Supports replication for high-availability setups
- **Partitioning**: Can split large tables for better performance
- **Future-Proof**: Architecture allows for easy expansion as needs grow

### Developer Experience

- **Standards Compliant**: Follows SQL standards closely
- **Rich Ecosystem**: Excellent Python support through psycopg2
- **Better Error Messages**: Clear, helpful error reporting
- **Advanced Data Types**: Arrays, JSONB, UUID, and custom types

### Comparison with Alternatives

| Feature | PostgreSQL | MySQL/MariaDB | SQLite |
|---------|-----------|---------------|---------|
| ACID Compliance | ✅ Full | ⚠️ Partial | ✅ Full |
| Concurrent Writes | ✅ Excellent | ⚠️ Good | ❌ Limited |
| Complex Queries | ✅ Excellent | ⚠️ Good | ⚠️ Basic |
| JSON Support | ✅ Native | ⚠️ Limited | ❌ No |
| Full-Text Search | ✅ Built-in | ⚠️ Basic | ⚠️ FTS5 |
| Security Features | ✅ Advanced | ⚠️ Good | ❌ Basic |
| Scalability | ✅ Excellent | ⚠️ Good | ❌ Limited |
| Network Support | ✅ Yes | ✅ Yes | ❌ No |

### Perfect for Password Management

PostgreSQL is ideal for a password manager because:

1. **Data Integrity**: ACID compliance ensures passwords are never lost or corrupted
2. **Performance**: Fast reads and writes even with encrypted data
3. **Security**: Enterprise-grade security features protect sensitive data
4. **Reliability**: Proven track record in mission-critical applications
5. **Flexibility**: Can easily add features like password history, sharing, or audit logs

---

## 📸 Screenshots

### Interactive Menu
```
╭──────────────────────────────────────────╮
│              Main Menu                   │
├──────────────────────────────────────────┤
│                                          │
│  1. Add New Password Entry               │
│  2. View All Entries                     │
│  3. Search & Extract Password            │
│  4. Delete Entry                         │
│  5. Generate Random Password             │
│  6. Exit                                 │
│                                          │
╰──────────────────────────────────────────╯
```

### Adding a Password
```
╭─────────────────────────────────────╮
│      ADD NEW PASSWORD ENTRY         │
╰─────────────────────────────────────╯

MASTER PASSWORD: ********

Enter the details:
🌐 Site Name: GitHub
🔗 Site URL: https://github.com
📧 Email (optional): user@example.com
👤 Username: myusername
Password: ****************

[+] Added entry
```

### Viewing Entries
```
                    Total Entries: 3
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Site Name  ┃ URL              ┃ Username      ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ GitHub     │ github.com       │ myusername    │
│ Gmail      │ gmail.com        │ john@gmail    │
│ Amazon     │ amazon.com       │ shopper123    │
└────────────┴──────────────────┴───────────────┘
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas for Improvement

- 🌐 Web-based GUI using Flask/Django
- 📱 Mobile app (Android/iOS)
- ☁️ Optional cloud sync with end-to-end encryption
- 🔄 Password change history
- 📊 Security audit and password strength analysis
- 🔐 Two-factor authentication (2FA)
- 📤 Import/export from other password managers
- 🌍 Multi-language support

---

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2026 Arghya Nayak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Contact

**Arghya Nayak** - [arghya05nayak@gmail.com](mailto:arghya05nayak@gmail.com)

Project Link: [https://github.com/arghya-nayak/CLI_Based_Password_Manager_Using_Python](https://github.com/arghya-nayak/CLI_Based_Password_Manager_Using_Python)

---

## 🙏 Acknowledgments

- **PyCryptodome** - Cryptographic library
- **Rich** - Beautiful terminal formatting
- **PostgreSQL** - Robust database system
- **Python Community** - For excellent libraries and documentation

---

## ⚠️ Security Disclaimer

This password manager is designed for educational purposes and personal use. While it implements industry-standard encryption and security practices, it has not undergone professional security auditing. 

**Recommendations:**
- Use a strong, unique master password
- Keep regular backups of your database
- Don't share your device secret or master password
- Use at your own risk

For critical or commercial use, consider professionally audited solutions like Bitwarden, 1Password, or KeePass.

---

## 📚 Additional Resources

- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PyCryptodome Documentation](https://pycryptodome.readthedocs.io/)

---

<div align="center">

**Made with ❤️ and Python**

⭐ Star this repository if you find it helpful!

</div>