"""
Author: Russell Johnson
Date 29 Nov 2025
SER416 Final Project
household.py
This class maintains all the data of a single household
"""

import pandas as pd
import cli_utils as cli
import sys
import numpy as np
from cli_utils import NA


#NA = "n/a"
# ------------------
# Static functions
# ------------------
def empty_dataframe() -> pd.DataFrame:
    """
    Makes a dataframe with just the correct column headers to hold household object data
    :return: empty dataframe
    """
    columns = [
        "address", "adults", "children", "pets", "dogs", "crit_meds", "ref_meds",
        "special_needs", "gas_tank", "gas_line", "adrs_number", "adrs_street",
        "adrs_city", "adrs_state", "adrs_zip", "med_training", "email", "phone",
        "know_nbr", "key_nbr", "news_ltr", "contact"
    ]
    return pd.DataFrame(columns=columns)

def is_valid_optional_string(x, length=None):
    """
    Checks if valid optional string data
    :param x: string to check:
    :param length: optional required length of string
    :return: true if valid
    """
    if isinstance(x, str):
        if length is None or len(x) == length:
            return True
    return False


def is_valid_optional_numeric(x, length=None):
    """
    Checks if valid optional numeric data. Can be just digits or n/a
    :param x: string to check
    :param length: optional required length of string
    :return: true if valid
    """
    if isinstance(x, str):
        if x == NA:
            return True
        if x.isdigit() and (length is None or len(x) == length):
            return True
    return False


def is_valid_optional_bool(x):
    """
    Checks if valid optional numeric data. Can be t,f, or n/a
    :param x: string to check
    :return: true if valid
    """
    if isinstance(x, str):
        if x.lower() == 't' or x.lower() == 'f' or x == NA:
            return True
    return False


def is_valid_string(x, length=None):
    """
    Checks if valid string. cannot be n/a
    :param x: string to check
    :param length: optional required length of string
    :return: true if valid
    """
    if isinstance(x, str):
        if x != NA and (length is None or len(x) == length):
            return True
    return False


def is_valid_numeric(x, length=None):
    """
    Checks if valid optional numeric data. Must be just digits
    :param x: string to check
    :param length: optional required length of string
    :return: true if valid
    """
    if isinstance(x, str):
        if x.isdigit() and (length is None or len(x) == length):
            return True
    return False


def is_valid_bool(x):
    """
    Checks if valid optional numeric data. Must be t or f
    :param x: string to check
    :return: true if valid
    """
    if isinstance(x, str):
        if x.lower() == 't' or x.lower() == 'f':
            return True
    return False

# ------------------
# Household class
# ------------------

class Household:
    def __init__(
            self,
            adults=None,
            children=None,
            pets=None,
            dogs=None,
            crit_meds=None,
            ref_meds=None,
            special_needs=None,
            gas_tank=None,
            gas_line=None,
            adrs_number=None,
            adrs_street=None,
            adrs_city=None,
            adrs_state=None,
            adrs_zip=None,
            med_training=None,
            email=None,
            phone=None,
            know_nbr=None,
            key_nbr=None,
            news_ltr=None,
            contact=None,
    ) -> None:
        """
        Initialize Household object
        """

        self.adults = adults
        self.children = children
        self.pets = pets
        self.dogs = dogs
        self.crit_meds = crit_meds
        self.ref_meds = ref_meds
        self.special_needs = special_needs
        self.gas_tank = gas_tank
        self.gas_line = gas_line
        self.adrs_number = adrs_number
        self.adrs_street = adrs_street
        self.adrs_city = adrs_city
        self.adrs_state = adrs_state
        self.adrs_zip = adrs_zip
        self.med_training = med_training
        self.email = email
        self.phone = phone
        self.know_nbr = know_nbr
        self.key_nbr = key_nbr
        self.news_ltr = news_ltr
        self.contact = contact
        self.validated = False
        self.adrs = None

    def validate_data(self) -> bool:
        """
        Checks the types of all data to make sure required data is input and optional data is no wrong type
        :return:
        """
        # Required data must be the correct type
        if not is_valid_numeric(self.adults):
            print(f"Validation Error: adults {self.adults}", file=sys.stderr)
            return False
        if not is_valid_numeric(self.children):
            print(f"Validation Error: children {self.children}", file=sys.stderr)
            return False
        if not is_valid_bool(self.pets):
            print(f"Validation Error: pets {self.pets}", file=sys.stderr)
            return False
        if not is_valid_bool(self.dogs):
            print(f"Validation Error: dogs {self.dogs}", file=sys.stderr)
            return False
        if not is_valid_bool(self.crit_meds):
            print(f"Validation Error: crit_meds {self.crit_meds}", file=sys.stderr)
            return False
        if not is_valid_bool(self.ref_meds):
            print(f"Validation Error: ref_meds {self.ref_meds}", file=sys.stderr)
            return False
        if not is_valid_bool(self.special_needs):
            print(f"Validation Error: special_needs {self.special_needs}", file=sys.stderr)
            return False
        if not is_valid_bool(self.gas_tank):
            print(f"Validation Error: gas_tank {self.gas_tank}", file=sys.stderr)
            return False
        if not is_valid_bool(self.gas_line):
            print(f"Validation Error: gas_line {self.gas_line}", file=sys.stderr)
            return False
        if not is_valid_string(self.adrs_number):
            print(f"Validation Error: adrs_number {self.adrs_number}", file=sys.stderr)
            return False
        if not is_valid_string(self.adrs_street):
            print(f"Validation Error: adrs_street {self.adrs_street}", file=sys.stderr)
            return False
        if not is_valid_string(self.adrs_city):
            print(f"Validation Error: adrs_city {self.adrs_city}", file=sys.stderr)
            return False
        if not is_valid_string(self.adrs_state, length=2):
            print(f"Validation Error: adrs_state {self.adrs_state} type", file=sys.stderr)
            return False
        if not is_valid_string(self.adrs_zip, length=5):
            print(f"Validation Error: adrs_zip {self.adrs_zip} type", file=sys.stderr)
            return False
        # optional data can also be NA
        if not is_valid_optional_bool(self.med_training):
            print(f"Validation Error: med_training {self.med_training}", file=sys.stderr)
            return False
        if not is_valid_optional_string(self.email):
            print(f"Validation Error: email {self.email}", file=sys.stderr)
            return False
        if not is_valid_optional_numeric(self.phone, length=10):
            print(f"Validation Error: phone {self.phone}", file=sys.stderr)
            return False
        if not is_valid_optional_bool(self.know_nbr):
            print(f"Validation Error: know_nbr {self.know_nbr}", file=sys.stderr)
            return False
        if not is_valid_optional_bool(self.key_nbr):
            print(f"Validation Error: key_nbr {self.key_nbr}", file=sys.stderr)
            return False
        if not is_valid_optional_bool(self.news_ltr):
            print(f"Validation Error: news_ltr {self.news_ltr}", file=sys.stderr)
            return False
        if not is_valid_optional_bool(self.contact):
            print(f"Validation Error: contact {self.contact}", file=sys.stderr)
            return False

        # If all checks pass update the address string and return true
        self.adrs = f"{self.adrs_number} {self.adrs_street}/{self.adrs_city},{self.adrs_state} {self.adrs_zip}"
        self.validated = True
        return True


    #def load_dataframe(self, df: pd.DataFrame) -> bool:
    def load_data(self, series: pd.Series) -> bool:
        """
        Populates data from a single row from a dataframe. Returns false if data is invalid or multi-line
        :param series: series of data from a pandas dataframe
        :return: true if valid, false if invalid
        """

        # Check if all required columns exist in the series
        required_columns = [
            'adults', 'children', 'pets', 'dogs', 'crit_meds', 'ref_meds', 'special_needs',
            'gas_tank', 'gas_line', 'adrs_number', 'adrs_street', 'adrs_city', 'adrs_state',
            'adrs_zip', 'med_training', 'email', 'phone', 'know_nbr', 'key_nbr', 'news_ltr', 'contact'
        ]
        if not all(col in series.index for col in required_columns):
            print("Error: load_data given series without all required data", file=sys.stderr)
            return False

        # load the data
        self.adults = series['adults']
        self.children = series['children']
        self.pets = series['pets']
        self.dogs = series['dogs']
        self.crit_meds = series['crit_meds']
        self.ref_meds = series['ref_meds']
        self.special_needs = series['special_needs']
        self.gas_tank = series['gas_tank']
        self.gas_line = series['gas_line']
        self.adrs_number = series['adrs_number']
        self.adrs_street = series['adrs_street']
        self.adrs_city = series['adrs_city']
        self.adrs_state = series['adrs_state']
        self.adrs_zip = series['adrs_zip']
        self.med_training = series['med_training']
        self.email = series['email']
        self.phone = series['phone']
        self.know_nbr = series['know_nbr']
        self.key_nbr = series['key_nbr']
        self.news_ltr = series['news_ltr']
        self.contact = series['contact']
        # check to make sure the data is valid
        if self.validate_data():
            return True
        else:
            print("Error: load_dataframe given invalid data", file=sys.stderr)
            return False

    def get_adrs_str(self):
        """
        Compiles all address data into a single-line string with a / between the street name and city info
        :return: compiled address string, none if address is invalid
        """
        if not self.validate_data(): return None
        return self.adrs

    def ask_questions(self, scr_w) -> None:
        """
        Asks the user the battery of questions to generate a new household object
        :param scr_w: the max width of the display
        :return: none
        """
        self.validated = False  # flag the data as unvalidated because it is changing
        req = "Add New Household: Required Questions"
        # Ask the required questions
        self.adults = cli.prompt_user(
            "How many adults live in your household?",
            header=req, input_format="int", row_limit=scr_w)
        self.children = cli.prompt_user(
            "How many children live in your household?",
            header=req, input_format="int", row_limit=scr_w)
        self.pets = cli.prompt_user(
            "Do you have pets?",
            header=req, input_format="y/n", row_limit=scr_w)
        if self.pets:
            self.dogs = cli.prompt_user(
                "Do you have any dogs?",
                header=req, input_format="y/n", row_limit=scr_w)
        else:  # Cannot have dogs if there are no pets
            self.dogs = False
        self.crit_meds = cli.prompt_user(
            "Does anyone in the household have critical medications?",
            header=req, input_format="y/n", row_limit=scr_w)
        if self.crit_meds:
            self.ref_meds = cli.prompt_user(
                "Do any of these medications need to be refrigerated?",
                header=req, input_format="y/n", row_limit=scr_w)
        else:  # Cannot have temp sensitive critical meds if there are no critical meds
            self.ref_meds = False
        self.special_needs = cli.prompt_user(
            "Does anyone in this household have special needs that would " +
            "require extra assistance in an evacuation?",
            header=req, input_format="y/n", row_limit=scr_w)
        self.gas_tank = cli.prompt_user(
            "Does the house have a large propane tank? Anything larger " +
            "than the standard size used in a gas grill?",
            header=req, input_format="y/n", row_limit=scr_w)
        self.gas_line = cli.prompt_user(
            "Does the house have gas line hookup, such as a gas stove, gas fireplace, or gas heat?",
            header=req, input_format="y/n", row_limit=scr_w)
        self.adrs_number = cli.prompt_user(
            "What is the number of the street address?" +
            " For example, if you lived on 123 Main Street, you would enter '123'",
            header=req, input_format="numeric", row_limit=scr_w)
        self.adrs_street = cli.prompt_user(
            "What is the name of the street your house is on?" +
            " For example, if you lived on 123 Main Street, you would enter 'Main Street'",
            header=req, row_limit=scr_w)
        self.adrs_city = cli.prompt_user(
            "What is the town/city/community name on your mailing address?" +
            " For example, if your address was was '123 Main Street Phoenix, AZ 12345' you would enter 'Phoenix'",
            header=req, row_limit=scr_w)
        self.adrs_state = cli.prompt_user(
            "What is 2 letter state abbreviation for your mailing address?" +
            " For example, if you live in Arizona you would enter 'AZ'",
            header=req, input_length=2, row_limit=scr_w)
        self.adrs_zip = cli.prompt_user(
            "What is 5 digit zip code on your mailing address?" +
            " For example, if your address was was '123 Main Street Phoenix, AZ 12345' you would enter '12345'",
            header=req, input_format="numeric", input_length=5, row_limit=scr_w)

        # optional questions
        opt = "Add New Household: Optional Question ( Enter nothing to skip )"  # header for the optional questions
        self.med_training = cli.prompt_user(
            "Does anyone in this household have medical training and would be able to render assistance in an " +
            "emergency?",
            header=opt, input_format="y/n", row_limit=scr_w, required=False)
        self.email = cli.prompt_user(
            "What is the best email address to update this household about active emergencies and "+
            "natural disasters?",
            header=opt, row_limit=scr_w, required=False)
        self.phone = cli.prompt_user(
            "What is the best phone number to contact this household in the event of an active emergency " +
            "and natural disaster? Enter just the digits of a 10 digit phone number, including area code. No symbols",
            header=opt, input_format="numeric", input_length=10, row_limit=scr_w, required=False)
        self.know_nbr = cli.prompt_user(
            "Do the members of this household know their neighbors?",
            header=opt, input_format="y/n", row_limit=scr_w, required=False)
        self.key_nbr = cli.prompt_user(
            "Does this household have a key to their neighbor's house?",
            header=opt, input_format="y/n", row_limit=scr_w, required=False)
        self.news_ltr = cli.prompt_user(
            "Would you like to receive the CERT newsletter to stay updated with information beyond currently " +
            "active emergencies and natural disasters?",
            header=opt, input_format="y/n", row_limit=scr_w, required=False)
        self.contact = cli.prompt_user(
            "May CERT use this contact information for anything other than communications directly related " +
            "to active emergencies and natural disasters?",
            header=opt, input_format="y/n", row_limit=scr_w, required=False)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Creates a panda's dataframe row of this object if it is valid. Otherwise, it returns none.
        :return: dataframe row
        """
        if not self.validate_data():
            print("Error: Household object not valid")
            return None
        dict = {
            "address": self.adrs,
            "adults": self.adults,
            "children": self.children,
            "pets": self.pets,
            "dogs": self.dogs,
            "crit_meds": self.crit_meds,
            "ref_meds": self.ref_meds,
            "special_needs": self.special_needs,
            "gas_tank": self.gas_tank,
            "gas_line": self.gas_line,
            "adrs_number": self.adrs_number,
            "adrs_street": self.adrs_street,
            "adrs_city": self.adrs_city,
            "adrs_state": self.adrs_state,
            "adrs_zip": self.adrs_zip,
            "med_training": self.med_training,
            "email": self.email,
            "phone": self.phone,
            "know_nbr": self.know_nbr,
            "key_nbr": self.key_nbr,
            "news_ltr": self.news_ltr,
            "contact": self.contact,
        }
        df = pd.DataFrame([dict])
        return df






def main():
    """
    This function is just used for dev demoing
    """

    print("Running in dev mode")

    # test one household
    hh = Household(
        adults="3",
        children="3",
        pets='t',
        dogs='t',
        crit_meds='f',
        ref_meds='f',
        special_needs='t',
        gas_tank='t',
        gas_line='f',
        adrs_number="742",
        adrs_street="Evergreen Terrace",
        adrs_city="Springfield",
        adrs_state="OR",
        adrs_zip="55555",
        med_training='f',
        email="el_barto@hotmail.com",
        phone="5035551234",
        know_nbr='t',
        key_nbr='f',
        news_ltr=NA,
        contact='f'
    )
    print(f"Is valid? {hh.validate_data()}")

    print(hh.to_dataframe().to_string())

    # test several households

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

    dataframes = []
    dataframes.append(hh0.to_dataframe())
    dataframes.append(hh1.to_dataframe())
    dataframes.append(hh2.to_dataframe())
    dataframes.append(hh3.to_dataframe())
    dataframes.append(hh4.to_dataframe())
    dataframes.append(hh5.to_dataframe())
    dataframes.append(hh6.to_dataframe())

    combined = pd.concat(dataframes)
    print(combined.to_string())


if __name__ == "__main__":
    main()
