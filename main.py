"""
main.py
Author: Russell Johnson
Date 22 Nov 2025
SER416 Final Project
This is the main file of the CERT household tracker project.
"""
import sqlite3
import os
import pandas as pd
import cli_utils as cli
from cli_utils import NA
import household as hh
from household import Household
import sys
import csv

# ------------------
# Constants
# ------------------

SQLITE_FILENAME = "cert.db"
TABLE_NAME = "households"
TERMINAL_WIDTH = 60


# ------------------
# Helper functions
# ------------------

def display_dataframe(df: pd.DataFrame) -> None:
    """
    Displays a dataframe of household object. Allows some elements to use a second row if space is needed
    :param df: dataframe to display
    """
    # hardcoded header
    col_labels = (
            "                                                         " +
            "                         Crt Ref Spc Gas Gas Med Knw Key Nws Con\n" +
            " address                         email             phone        " +
            "Adlt Kids Pts Dog Med Med Nds Tnk Ln  Tng Nbr Nbr Ltr tct "
    )
    row_count, col_count = df.shape
    # exit early if no data is in the dataframe
    if (row_count == 0):
        print(col_labels)
        print("\n*** No data loaded ***\n")
        return

    # create dict of data labels and max allowed lengths
    col_dict = {'address': 30,
                'email': 15,
                'phone': 10,
                'adults': 2,
                'children': 2,
                'pets': 1,
                'dogs': 1,
                'crit_meds': 1,
                'ref_meds': 1,
                'special_needs': 1,
                'gas_tank': 1,
                'gas_line': 1,
                'med_training': 1,
                'know_nbr': 1,
                'key_nbr': 1,
                'news_ltr': 1,
                'contact': 1}
    # iterate through each entry in the dataframe
    print("*** Displaying Currently Loaded Data *** \n")
    for row_index in range(row_count):
        # show the col headers every 10 lines
        if row_index % 10 == 0:
            print(col_labels)
        # create empty strings to build the first and possible second line of this row
        first_line = ""
        second_line = ""
        use_second_line = False
        # go through each column. Note, not all columns will be displayed, this gets a little complicated
        for col_name in col_dict.keys():
            # cast the contents of that element to a string
            contents = str(df.iloc[row_index, df.columns.get_loc(col_name)])
            width_limit = col_dict[col_name]  # create new variable for readability
            if contents == NA:  # if the element was unanswered, write n/a
                if width_limit == 1:  # for small columns do not use left & right whitespace
                    first_line += f"{'n/a': <{width_limit + 1}}|"
                    second_line += f" {'': <{width_limit}} |"  # put a blank on the second line
                else:  # for all other columns use right whitespace
                    first_line += f" {'n/a': <{width_limit + 1}}|"
                    second_line += f" {'': <{width_limit}} |"  # put a blank on the second line
            elif contents == 't':  # to make the trues stand out use capitols
                first_line += f" {'T': <{width_limit}} |"
                second_line += f" {'': <{width_limit}} |"  # put a blank on the second line
            elif len(contents) <= width_limit:  # if it fits in the width limit
                first_line += f" {contents: <{width_limit}} |"
                second_line += f" {'': <{width_limit}} |"  # put a blank on the second line
            else:  # if the second line is needed
                use_second_line = True
                first_line += f" {contents[:width_limit]: <{width_limit}}-|"
                second_line += f"  {contents[width_limit:width_limit * 2 - 1]: <{width_limit}}|"
            pass
        print(first_line)
        if use_second_line:
            print(second_line)
    print()  # do a line break for readability


def df_to_options(df: pd.DataFrame) -> list[str]:
    """
    Creates a list of strings based on the address from the dataframe of household data
    :param df:
    :return: string of 1-line addresses
    """
    return df['address'].tolist()


def add_household_to_df(household: Household, df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dataframe object from the household, checks to see there is no household with the
    same address string. If there is no match then it adds the new dataframe to the given dataframe
    :param household: the Household object to add
    :param df: the Dataframe to add it too
    :return: updated dataframe or original dataframe if there was an error
    """
    # Convert the household to a DataFrame
    new_row = household.to_dataframe()

    # check to see that the data was valid and a dataframe was actually created
    if new_row is None:
        print("Error: add_household_to_df given an invalid Household object", file=sys.stderr)
        return df  # return the dataframe unedited

    # Get the address string from the new household
    new_address = new_row.iloc[0]['address']

    # Check if this address already exists in the dataframe
    if new_address in df['address'].values:  # Duplicate address found
        print("Error: add_household_to_df given duplicate address", file=sys.stderr)
        return df  # return the dataframe unedited
    else:  # add it and return the updated dataframe
        return pd.concat([df, new_row], ignore_index=True)


def get_household_from_df(address: str, df: pd.DataFrame) -> Household:
    """
    Scans the dataframe for a household with a matching address. If one is found it returns
    a Household object from that row
    :param address: "[street number] [street name],[city],[2 letter state] [5 number zip]"
    :param df: Dataframe built from household object data
    :return: if match found: household object, if no match: None
    """
    # Find the row with the matching address. Should only be 1 row
    matching_rows = df[df['address'] == address]

    if matching_rows.empty:
        print("Error: get_household_from_df given address not in dataframe", file=sys.stderr)
        return df  # return the original dataframe

    # Addresses are unqiue, so the 1st one should be the only one
    row = matching_rows.iloc[0]

    # Create a new Household object from the row data
    household = Household()
    household.load_data(row)
    return household


def remove_household_from_df(address: str, df: pd.DataFrame) -> Household:
    """
    Scans the dataframe for a household with a matching address. If one is found it removes
    that row from the dataframe, if no match is found then it returns None
    :param address: "[street number] [street name]/[city],[2 letter state] [5 number zip]"
    :param df: Dataframe to remove row from
    :return: if match found: true, if no match: false
    """
    # Find the row with the matching address. Should only be 1 row
    delete_row_index = df.index[df['address'] == address]

    if delete_row_index.empty:
        print("Error: remove_household_from_df given address not in dataframe", file=sys.stderr)
        return df  # return the original dataframe

    # drop the 1st (and should be only) row that was identified to be removed
    return df.drop(delete_row_index[0])


def merge_dataframes(df_original: pd.DataFrame, df_new: pd.DataFrame) -> pd.DataFrame:
    """
    Merges 2 dataframes. Checks against duplicates. Does not validate data
    :param df_original: Dataframe to be merged into
    :param df_new: dataframe to be merged
    :return: merged dataframe
    """
    # Filter df_new to only include rows with addresses not in frame_old
    new_rows = df_new[~df_new['address'].isin(df_original['address'])]

    # Merge the dataframes
    merged = pd.concat([df_original, new_rows], ignore_index=True)
    return merged


def save_to_sql(df: pd.DataFrame) -> bool:
    """
    Saves household dataframe to sqlite database on hard drive
    :param df: dataframe to save
    :return: true if save successful
    """
    print("FILE OPERATION: Opening Database")
    try:
        # connect to sqlite database
        db_conn = sqlite3.connect(SQLITE_FILENAME)
        # create a table
        print("FILE OPERATION: Writing to Database")
        df.to_sql(TABLE_NAME, db_conn, if_exists="replace", index=False)
        db_conn.close()
        print("FILE OPERATION: Database Write Complete")
        return True
    except sqlite3.Error as e:
        print(f"Error: could not complete write operation - {e}", file=sys.stderr)
        db_conn.close()
        return False


def scan_for_csv() -> list[str]:
    """
    Scans the directory the program is in for CSV file. Checks each file for the correct headers.
    Returns a list of valid filenames
    :return: list of valid filenames
    """
    # Define headers
    correct_headers = {
        'address', 'adults', 'children', 'pets', 'dogs', 'crit_meds',
        'ref_meds', 'special_needs', 'gas_tank', 'gas_line', 'adrs_number',
        'adrs_street', 'adrs_city', 'adrs_state', 'adrs_zip', 'med_training',
        'email', 'phone', 'know_nbr', 'key_nbr', 'news_ltr', 'contact'
    }

    valid_csvs = []

    # Get all files in current directory
    current_dir = os.getcwd()
    for filename in os.listdir(current_dir):
        # filter for file type
        if filename.endswith('.csv'):
            file_path = os.path.join(current_dir, filename)
            # Check for valid headers
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    headers = next(reader, None)
                    # Check if headers exist and match
                    if headers:
                        header_set = {header.strip() for header in headers}
                        if correct_headers.issubset(header_set):
                            valid_csvs.append(filename)

            except (IOError, csv.Error):
                # not an error worth reporting to the user
                continue
    return valid_csvs


# ------------------
# Main program
# ------------------
def main():
    empty_df = hh.empty_dataframe()  # DEBUG

    # create properly headered empty dataframe to hold data in the program
    household_df = hh.empty_dataframe()

    # check to see if database exists
    if os.path.exists(SQLITE_FILENAME):  # if the db exists
        print("Starting Up: Database Found")  # debug
        db_connection = sqlite3.connect(SQLITE_FILENAME)

        # check if table exists in database
        try:
            cursor = db_connection.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """, (TABLE_NAME,))
            result = cursor.fetchone()

            if result:
                print("Starting Up: Database Table Found")
                # Use pd.read_sql instead of pd.read_sql_table for SQLite
                household_df = pd.read_sql(f'SELECT * FROM "{TABLE_NAME}"', db_connection)
                print("Starting Up: Data Loaded")
            else:
                print("Starting Up: Database Table NOT Found")
                print("Starting Up: Creating Database Table")
                household_df.to_sql(TABLE_NAME, db_connection, if_exists='replace', index=False)
                print("Starting Up: Database Table Created")
        except sqlite3.Error as e:
            print(f"Error checking table existence: {e}")
            db_connection.close()
        finally:
            db_connection.close()

    else:  # create it if it does not
        print("Starting Up: Database NOT Found")
        db_connection = sqlite3.connect(SQLITE_FILENAME)
        household_df.to_sql(TABLE_NAME, db_connection, if_exists='replace', index=False)
        print("Starting Up: Database Created")
        db_connection.close()

    # ------------------
    # Main Loop
    # ------------------
    while True:
        # main screen
        main_menu_options = [
            "View households",
            "Add a household",
            "Remove a household",
            "Edit a household",
            "Import CSV file",
            "Export CSV file",
            "Save Changes to Database",
            "Save & Exit",
            "Exit & Discard all changes"
        ]

        # prompt the user to make a main menu selection
        main_menu_choice = cli.prompt_user("Main Menu", user_options=main_menu_options)
        #main_menu_choice = "View households"

        # handle main menu options
        if main_menu_choice == "View households":
            cli.clear_screen()
            display_dataframe(household_df)
            input(f"Press enter to continue")

        if main_menu_choice == "Add a household":
            # create a new household object and prompt the user to fill it out
            new_hh = Household()
            new_hh.ask_questions(TERMINAL_WIDTH)
            # add that household to the active dataframe
            household_df = add_household_to_df(new_hh, household_df)
            # show updated active dataframe to user
            cli.clear_screen()
            display_dataframe(household_df)
            input(f"Added {new_hh.get_adrs_str()}. Press enter to continue")

        elif main_menu_choice == "Remove a household":
            # ask user which household to delete
            delete_options = df_to_options(household_df)
            user_delete_choice = cli.prompt_user("Pick one to remove:", user_options=delete_options)
            # confirm user wants to delete household
            if cli.prompt_user("Delete Selected Entry?", input_format="y/n", header=user_delete_choice):
                household_df = remove_household_from_df(user_delete_choice, household_df)
                # show updated active dataframe to user
                cli.clear_screen()
                display_dataframe(household_df)
                input(f"Removed {user_delete_choice}. Press enter to continue")
            else:
                input("Deletion Canceled. Press enter to continue.")

        elif main_menu_choice == "Edit a household":
            # ask user which household to edit
            edit_options = df_to_options(household_df)
            user_delete_choice = cli.prompt_user("Pick one to Edit:", user_options=edit_options)
            # confirm user wants to edit household
            if cli.prompt_user("Edit Selected Entry?", input_format="y/n", header=user_delete_choice):
                # delete old old household
                household_df = remove_household_from_df(user_delete_choice, household_df)
                # get edited household
                new_hh = Household()
                new_hh.ask_questions(TERMINAL_WIDTH)
                household_df = add_household_to_df(new_hh, household_df)
                # show updated active dataframe to user
                cli.clear_screen()
                display_dataframe(household_df)
                input(
                    f"Updated {user_delete_choice} with new record for {new_hh.get_adrs_str()}. Press enter to continue")
            else:
                input("Edit Canceled. Press enter to continue.")

        elif main_menu_choice == "Import CSV file":
            import_options = scan_for_csv()
            # back out if there are no valid files
            print(len(import_options))  # debug

            if len(import_options) == 0:
                input("No valid files in this directory. Press enter to continue")
            else:
                # create a new dataframe to hold the imported data
                new_df = hh.empty_dataframe()
                # prompt user for which file to read
                user_import_choice = cli.prompt_user("Select a file", user_options=import_options, header="Import CSV")
                new_df = pd.read_csv(user_import_choice, keep_default_na=False,
                                     na_filter=False)  # supress converting "n/a" from a string

                # let user determine to merge or overwrite data
                cli.clear_screen()
                print("Data imported from CSV:")
                display_dataframe(new_df)
                merge = input("Merge new data with current data or"
                              " overwrite current data with new data? [Enter \"Merge\" or \"Overwrite\"]")

                # clear console for readability
                cli.clear_screen()

                # if the user entered O then overwrite
                if len(merge) > 0:  # check that the user entered something
                    if merge[0].lower() == 'o':  # drop the old data and replace it with new
                        household_df = new_df
                        print(f"FILE OPERATION: Data overwritten")
                    else:
                        household_df = merge_dataframes(household_df, new_df)
                        print(f"FILE OPERATION: Data Merged")
                else:  # if no input then just cancel the import
                    print(f"FILE OPERATION: Import Canceled")
                display_dataframe(household_df)
                input(f"Press enter to continue")

        elif main_menu_choice == "Export CSV file":
            #Prompt user for export filename
            raw_name = cli.prompt_user("Enter the name of the file without the file extension. Use only letters and "
                                       "numbers. No spaces or symbols.", header="Export to CSV file")
            # remove any symbols so the filename is usable
            stripped_name = ''.join(filter(str.isalnum, raw_name)) + ".csv"
            # ask the user if that name is acceptable
            if cli.prompt_user(f"Confirm: export to file {stripped_name}",
                               header="Export to CSV file", input_format='y/n') == 't':
                household_df.to_csv(stripped_name, index=False)
                print(f"FILE OPERATION: Data exported to {stripped_name}")
            else:
                print(f"FILE OPERATION: Export Canceled")
            input(f"Press enter to continue")

        elif main_menu_choice == "Save Changes to Database":
            save_to_sql(household_df)
            input("Press enter to continue.")

        elif main_menu_choice == "Save & Exit":
            if save_to_sql(household_df):
                print("Changes saved to database.")
                print("Goodbye.")
                sys.exit(0)
            else:
                input("Error: Could not save. Try again or exit without saving. Push enter to continue.")

        elif main_menu_choice == "Exit & Discard all changes":
            print("Discarding all unsaved changes and exiting. Goodbye.")
            sys.exit(0)


if __name__ == "__main__":
    main()
