"""
main.py
Author: Russell Johnson
Date 22 Nov 2025
SER416 Final Project
This is the main file of the CERT household tracker project.
"""
import pprint as pp

import pandas as pd
import cli_utils as cli
from cli_utils import NA
#import household as hh
from household import Household
import sys

# ------------------
# Constants
# ------------------

SQLITE_FILENAME = "cert.db" # TODO: consider making this configurable by the user
I_CSV_FILENAME = "import.csv" # TODO: this MUST be configurable by the user
O_CSV_FILENAME = "output.csv" # TODO: this MUST be configurable by the user


# ------------------
# Helper functions
# ------------------

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
        return df # return the original dataframe

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
    print(delete_row_index)

    if delete_row_index.empty:
        print("Error: remove_household_from_df given address not in dataframe", file=sys.stderr)
        return df # return the original dataframe

    # drop the 1st (and should be only) row that was identified to be removed
    return df.drop(delete_row_index[0])


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
    med_training=NA, email="hh3@example.org", phone="5559876543",
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


test = hh0.to_dataframe()

print(test.to_string())

test = add_household_to_df(hh1, test)
test = add_household_to_df(hh2, test)
test = add_household_to_df(hh3, test)
test = add_household_to_df(hh4, test)
test = add_household_to_df(hh5, test)
test = add_household_to_df(hh6, test)
test = add_household_to_df(hh7, test)

print(test.to_string())

options = df_to_options(test)


#user_choice =   cli.prompt_user("Pick one:", user_options=options)
user_choice =1
cli.display_menu ("Pick one:", options=options, row_max=60)


print(f"You selected #{user_choice}\n{get_household_from_df(options[user_choice], test)}")

print (test)
test = remove_household_from_df(options[0], test)

print(test      )

test.to_csv( I_CSV_FILENAME, index=False)


sys.exit(0)

scr_w = 60

while True:
    # main screen
    main_options = [
        "Add a household",
        "Import CSV file",
        "Export CSV file",
        "Exit"
    ]

    user_input = cli.prompt_user("Main Menu", user_options=main_options)

    print(main_options.index("Add a household"))

    if user_input - 1 == main_options.index("Add a household"):
        new_hh = Household()
        new_hh.ask_questions(scr_w)

        df = new_hh.to_dataframe()
        print("test")
        print(df.to_string())

        input("press enter to continue")

    if user_input == 4:
        break
