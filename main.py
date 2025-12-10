"""
main.py
Author: Russell Johnson
Date 22 Nov 2025
SER416 Final Project
This is the main file of the CERT household tracker project.
"""
import pprint as pp
import sqlite3
import os

import pandas as pd
import cli_utils as cli
from cli_utils import NA
import household as hh
from household import Household
import sys
import textwrap

# ------------------
# Constants
# ------------------

SQLITE_FILENAME = "cert.db"  # TODO: consider making this configurable by the user
I_CSV_FILENAME = "import.csv"  # TODO: this MUST be configurable by the user
O_CSV_FILENAME = "output.csv"  # TODO: this MUST be configurable by the user
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
            "                                                                                  Crt Ref Spc Gas Gas Med Knw Key Nws Con\n" +
            " address                         email             phone        Adlt Kids Pts Dog Med Med Nds Tnk Ln  Tng Nbr Nbr Ltr tct "
    )
    row_count, col_count = df.shape
    # exit early if no data is in the dataframe
    if (row_count == 0):
        print(col_labels)
        print("No data loaded")
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
    for row_index in range(row_count):
        # show the col headers every 10 lines
        if row_index % 10 == 0:
            print(col_labels)
        # create empty strings to build the first and possible second line of this row
        first_line = ""
        second_line = ""
        use_second_line = False
        # go through each column. Note, not all columns will be displayed
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


def add_household_to_df(household: Household, df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dataframe object from the household, checks to see there is no household with the
    same address string. If there is no match then it adds the new dataframe to the given dataframe
    :param household: the Household object to add
    :param df: the Dataframe to add it too
    :return: updated dataframe or orginial dataframe if there was an error
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


def df_to_options(df: pd.DataFrame) -> list[str]:
    """
    Creates a list of strings based on the address from the dataframe of household data
    :param df:
    :return: string of 1-line addresses
    """
    return df['address'].tolist()


def get_household_from_df(address: str, df: pd.DataFrame) -> Household:
    """
    Scans the dataframe for a household with a matching address. If one is found it returns
    a Household object from that row
    :param address: "[street number] [street name]/[city],[2 letter state] [5 number zip]"
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


# TODO: delete this debugging data
hh0 = Household(
    adults="2", children="0", pets="f", dogs="f",
    crit_meds="f", ref_meds="f", special_needs="f",
    gas_tank="f", gas_line="f",
    adrs_number="100", adrs_street="Maple Ave", adrs_city="Springfield",
    adrs_state="AA", adrs_zip="12345",
    med_training=NA, email=NA, phone=NA,
    know_nbr=NA, key_nbr=NA, news_ltr=NA, contact=NA
)

hh1 = Household(
    adults="1", children="2", pets="t", dogs="t",
    crit_meds="t", ref_meds="t", special_needs="f",
    gas_tank="t", gas_line="f",
    adrs_number="101", adrs_street="Oak St", adrs_city="Springfield",
    adrs_state="AA", adrs_zip="12345",
    med_training="t", email="hh1@example.com", phone="5551234567",
    know_nbr="t", key_nbr="f", news_ltr="t", contact="f"
)

hh2 = Household(
    adults="3", children="1", pets="f", dogs="f",
    crit_meds="f", ref_meds="f", special_needs="t",
    gas_tank="f", gas_line="t",
    adrs_number="102", adrs_street="Pine Rd", adrs_city="Springfield",
    adrs_state="AA", adrs_zip="12345",
    med_training="f", email=NA, phone=NA,
    know_nbr="f", key_nbr="t", news_ltr="f", contact="t"
)

hh3 = Household(
    adults="2", children="3", pets="t", dogs="f",
    crit_meds="f", ref_meds="f", special_needs="f",
    gas_tank="f", gas_line="f",
    adrs_number="103", adrs_street="Cedar Ln", adrs_city="Springfield",
    adrs_state="AA", adrs_zip="12345",
    med_training=NA, email="coolguy42@hotmail.com", phone="5559876543",
    know_nbr=NA, key_nbr=NA, news_ltr=NA, contact=NA
)

hh4 = Household(
    adults="1", children="0", pets="f", dogs="f",
    crit_meds="t", ref_meds="f", special_needs="f",
    gas_tank="f", gas_line="f",
    adrs_number="104", adrs_street="Birch Blvd", adrs_city="Springfield",
    adrs_state="AA", adrs_zip="12345",
    med_training="t", email=NA, phone=NA,
    know_nbr="f", key_nbr="f", news_ltr="f", contact="f"
)

hh5 = Household(
    adults="4", children="2", pets="t", dogs="t",
    crit_meds="f", ref_meds="f", special_needs="t",
    gas_tank="t", gas_line="t",
    adrs_number="105", adrs_street="Elm St", adrs_city="Springfield",
    adrs_state="AA", adrs_zip="12345",
    med_training="f", email="hh5@example.net", phone="5551112222",
    know_nbr="t", key_nbr="t", news_ltr="t", contact="t"
)

hh6 = Household(
    adults="2", children="1", pets="f", dogs="f",
    crit_meds="f", ref_meds="f", special_needs="f",
    gas_tank="f", gas_line="f",
    adrs_number="106", adrs_street="Willow Way", adrs_city="Springfield",
    adrs_state="AA", adrs_zip="12345",
    med_training=NA, email=NA, phone=NA,
    know_nbr=NA, key_nbr=NA, news_ltr=NA, contact=NA
)

hh7 = Household(
    adults="3", children="0", pets="t", dogs="f",
    crit_meds="t", ref_meds="t", special_needs="f",
    gas_tank="f", gas_line="t",
    adrs_number="107", adrs_street="Poplar Pl", adrs_city="Springfield",
    adrs_state="AA", adrs_zip="12345",
    med_training="t", email="hh7@example.com", phone="5553334444",
    know_nbr="f", key_nbr="f", news_ltr="f", contact="f"
)

hh8 = Household(
    adults="2", children="2", pets="f", dogs="f",
    crit_meds="f", ref_meds="f", special_needs="f",
    gas_tank="f", gas_line="f",
    adrs_number="108", adrs_street="Ash Ct", adrs_city="Springfield",
    adrs_state="AA", adrs_zip="12345",
    med_training="f", email=NA, phone=NA,
    know_nbr="t", key_nbr="t", news_ltr="t", contact="t"
)

hh9 = Household(
    adults="1", children="1", pets="t", dogs="t",
    crit_meds="f", ref_meds="f", special_needs="t",
    gas_tank="t", gas_line="f",
    adrs_number="109", adrs_street="Chestnut Dr", adrs_city="Springfield",
    adrs_state="AA", adrs_zip="12345",
    med_training="t", email="hh9@example.org", phone="5555556666",
    know_nbr="f", key_nbr="t", news_ltr="f", contact="f"
)


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

    # create empty database if none exists

    # load database into program's main dataframe

    # TODO: replace this with reading from a database
    household_df = add_household_to_df(hh1, household_df)
    household_df = add_household_to_df(hh2, household_df)
    household_df = add_household_to_df(hh3, household_df)
    household_df = add_household_to_df(hh4, household_df)
    household_df = add_household_to_df(hh5, household_df)
    household_df = add_household_to_df(hh6, household_df)
    household_df = add_household_to_df(hh7, household_df)

    while True:
        # main screen
        main_menu_options = [
            "View households",
            "Add a household",
            "Remove a household",
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
            display_dataframe(household_df)
            print("*********")
            display_dataframe(empty_df)

            print()
            input(f"Press enter to continue")

        if main_menu_choice == "Add a household":
            # TODO: make this add to the db, not just the df
            new_hh = Household()
            new_hh.ask_questions(TERMINAL_WIDTH)

            household_df = add_household_to_df(new_hh, household_df)
            print(household_df.to_string())
            input(f"Added {new_hh.get_adrs_str()}. Press enter to continue")

        elif main_menu_choice == "Remove a household":
            # TODO: make this remove from the db, not just the df
            delete_options = df_to_options(household_df)
            user_delete_choice = cli.prompt_user("Pick one to remove:", user_options=delete_options)
            if cli.prompt_user("Delete Selected Entry?", input_format="y/n", header=user_delete_choice):
                household_df = remove_household_from_df(user_delete_choice, household_df)
                print(household_df.to_string())
                input(f"Removed {user_delete_choice}. Press enter to continue")
            else:
                input("Deletion Canceled. Press enter to continue.")

        elif main_menu_choice == "Save & Exit":
            # TODO: make an graceful exit that saves data
            print("Changes saved to database.")
            print("Goodbye.")
            # db_connection close or something
            sys.exit(0)

        elif main_menu_choice == "Exit & Discard all changes":
            print("Discarding all unsaved changes and exiting. Goodbye.")
            sys.exit(0)


if __name__ == "__main__":
    main()
