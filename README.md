# cert-household-tracker
Final Project for SER416. Questionnaire and database system to gather and store information on households for rescue teams during natural disasters.

screencast link https://youtu.be/YVdZIkMrrzs



# CERT Household Tracker

## Overview

The **CERT Household Tracker** is a command‑line tool for collecting, managing, and storing information about households that participate in a Community Emergency Response Team (CERT).  It stores the data in a SQLite database, provides CSV import/export capabilities, and offers a simple interactive menu for viewing, adding, editing, and removing records.

## Table of Contents

1. [Features](#features)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Running the Application](#running-the-application)
5. [CSV Import / Export](#csv-import--export)
6. [Database Persistence](#database-persistence)


---

## Features

- A reusalbe, modular CLI interface library writen by me for this project, but is generic enough to be used in any CLI project. 
- Validation of required and optional fields with clear error messages.
- Automatic generation of a formatted address string.
- Storage of all records in a SQLite database (`cert.db`).
- CSV import with header validation and optional merge/overwrite handling.
- CSV export with sanitised file names.
- Ability to edit or delete existing household entries.

---

## System Requirements

| Component | Minimum Version |
|-----------|-----------------|
| Python    | 3.8 or later |
| pandas    | 1.5.0 |
| numpy     | 1.23.0 |
| SQLite    | Built‑in with Python distribution |

All other required modules (`cli_utils`, `household`) are part of the project repository.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/russcraftscode/cert-household-tracker
   cd cert-household-tracker
   ```

2. **Install dependencies**

   ```bash
   pip install pandas 
   pip install numpy
   ```


---

## Running the Application

```bash
python main.py
```

Note: This program starts with **NO DATA**. The program will create a blank database the first time it opens, but the user must provide all the data.  
The user can do this by one of two ways:
1. Entering the data in manually with the *Add a Household* menu option.
2. Importing data from the supplied CSV.  

CSV files are how this program imports and exports data, but are not used for long term storage. Stored data is kept in a SQLite database.  
Every time the program starts it checks its database for data. When directed to by the user, or when performing a save and quit, the updated data is writen back to the database.  


All boolean fields use the canonical values `'t'` (true), `'f'` (false), and `'n/a'` for “not applicable”.  
This was done so that python could differentiate between not answered and false, because python is "falsy" with its Nones  

---

## CSV Import / Export

### Import

1. Place a CSV file in the program’s working directory.
2. This program is only compatible with CSV files it has created.
3. Choose **Import CSV file** from the main menu.
4. Select the desired file from the presented list. Only compatible files in the same directory as this program will be shown.
5. Choose **Merge** to add only non‑duplicate records, or **Overwrite** to replace the current dataset entirely. Also, you can just hit **Enter** to cancel the import.

### Export

1. Choose **Export CSV file** from the main menu.
2. Provide a filename (letters and numbers only; spaces and symbols are stripped).
3. Confirm the export. The program writes a UTF‑8 CSV file with the same column layout used internally.

---

## Database Persistence

- The SQLite database file is named `cert.db`.
- On first run the program creates the database and a single table called `households`.
- Selecting **Save Changes to Database** writes the current in‑memory DataFrame to the table, overwriting any previous content.
- **Save & Exit** performs the same operation before terminating.
- **Exit & Discard all changes** terminates without writing to the database.

---

## Thanks for Checking Out My Project

This was much more complicated than I was expecting for what seemed like a simple CLI application. Overcoming hurdles and unexpected complexities helped to reinforce the topics covered in SER416
