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
import household as hh
from household import Household
import sys


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


def get_household_from_df(address: str, df: pd.DataFrame) -> hh.Household:
    """
    Scans the dataframe for a household with a matching address. If one is found it returns
    a Household object from that row
    :param address: "[stree number] [street name]/[city],[2ltr state] [5 number zip]"
    :param df: Dataframe built from household object data
    :return: if match found: household object, if no match: None
    """
    # Find the row with the matching address
    matching_rows = df[df['address'] == address]

    if matching_rows.empty:
        print("Error: get_household_from_df given address not in dataframe", file=sys.stderr)
        return None

    # Addresses are unqiue, so the 1st one should be the only one
    row = matching_rows.iloc[0]

    # Create a new Household object from the row data
    household = hh.Household()
    household.load_data(row)
    return household


def remove_household_from_df(address: str, df: pd.DataFrame) -> bool:
    """
    Scans the dataframe for a household with a matching address. If one is found it removes
    that row from the dataframe, if no match is found then it returns False
    :param address: "[stree number] [street name]/[city],[2ltr state] [5 number zip]"
    :param df: Dataframe to remove row from
    :return: if match found: true, if no match: false
    """
    # Find the row with the matching address
    delete_row_indexs = df.index[df['address'] == address]
    print(delete_row_indexs)

    return False


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

hh2 = hh.Household(
    adults="3", children="1", pets="f", dogs="f",
    crit_meds="f", ref_meds="f", special_needs="t",
    gas_tank="f", gas_line="t",
    adrs_number="102", adrs_street="Pine Rd", adrs_city="Springfield",
    adrs_state="AA", adrs_zip="12345",
    med_training="f", email=NA, phone=NA,
    know_nbr="f", key_nbr="t", news_ltr="f", contact="t"
)

hh3 = hh.Household(
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
        new_hh = hh.Household()
        """print(f"hh is valid {new_hh.validate_data()}") # DEBUG
        req = "Required Questions"
        # Ask the required questions
        new_hh.adults = cli_gui.prompt_user(
            "How many adults live in your household?",
            header=req, input_format="numeric", row_limit=scr_w)
        new_hh.children = cli_gui.prompt_user(
            "How many children live in your household?",
            header=req, input_format="numeric", row_limit=scr_w)
        new_hh.pets = cli_gui.prompt_user(
            "Do you have pets?",
            header=req, input_format="y/n", row_limit=scr_w)
        if new_hh.pets:
            new_hh.dogs = cli_gui.prompt_user(
                "Do you have any dogs?",
                header=req, input_format="y/n", row_limit=scr_w)
        else:# Cannot have dogs if there are no pets
            new_hh.dogs = False
        new_hh.crit_meds = cli_gui.prompt_user(
            "Does anyone in the household have critical medications?",
            header=req, input_format="y/n", row_limit=scr_w)
        if new_hh.crit_meds:
            new_hh.ref_meds = cli_gui.prompt_user(
                "Do any of these medications need to be refrigerated?",
                header=req, input_format="y/n", row_limit=scr_w)
        else: # Cannot have temp sensitive critical meds if there are no critical meds
            new_hh.ref_meds = False
        new_hh.special_needs = cli_gui.prompt_user(
            "Does anyone in this household have special needs that would require extra assistance in an evacuation?",
            header=req, input_format="y/n", row_limit=scr_w)
        new_hh.gas_tank = cli_gui.prompt_user(
            "Does the house have a large propane tank? Anything larger than the standard size used in a gas grill?",
            header=req, input_format="y/n", row_limit=scr_w)
        new_hh.gas_line = cli_gui.prompt_user(
            "Does the house have gas hookup for cooking or gas heat?",
            header=req, input_format="y/n", row_limit=scr_w)
        new_hh.ad_first = cli_gui.prompt_user(
            "What is the 1st line of the mailing address? Enter it as you would on an envelope,"+
            " street number and then street name",
            header=req, required=False, row_limit=scr_w)
        new_hh.ad_second = cli_gui.prompt_user(
            "What is the 2nd line of the mailing address? Enter it as you would on an envelope,"+
            " town name, then a comma, then state and zip code",
            header=req, required=False, row_limit=scr_w)

        # optional questions
        opt = "Optional Question ( Enter nothing to skip )"  # header for the optional questions
        new_hh.med_training = cli_gui.prompt_user(
            "Does anyone in this household have medical training and would be able to render assistance in an "
            "emergency?",
            header=opt, input_format="y/n", row_limit=scr_w, required=False)
        new_hh.email = cli_gui.prompt_user(
            "What is the best email address to update this household about active emergencies and natural disasters?",
            header=opt, row_limit=scr_w, required=False)
        new_hh.phone = cli_gui.prompt_user(
            "What is the best phone number to contact this household in the event of an active emergency and natural "
            "disaster?",
            header=opt, row_limit=scr_w, required=False)
        new_hh.know_nbr = cli_gui.prompt_user(
            "Do the members of this household know their neighbors?",
            header=opt, input_format="y/n", row_limit=scr_w, required=False)
        new_hh.key_nbr = cli_gui.prompt_user(
            "Does this household have a key to their neighbor's house?",
            header=opt, input_format="y/n", row_limit=scr_w, required=False)
        new_hh.news_ltr = cli_gui.prompt_user(
            "Would you like to receive the CERT newsletter to stay updated with information beyond currenlty active "
            "emergencies and natural disasters?",
            header=opt, input_format="y/n", row_limit=scr_w, required=False)
        new_hh.contact = cli_gui.prompt_user(
            "May CERT use this contact information for anything other than communications directly related to active "
            "emergencies and natural disasters?",
            header=opt, input_format="y/n", row_limit=scr_w, required=False)"""

        new_hh.ask_questions(scr_w)

        df = new_hh.to_dataframe()
        print("test")
        print(df.to_string())

        input("press enter to continue")

    if user_input == 4:
        break
