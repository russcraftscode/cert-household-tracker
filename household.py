"""
Author: Russell Johnson
Date 29 Nov 2025
SER416 Final Project
household.py
This class maintains all the data of a single household
"""

import pandas as pd

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
            ad_first=None,
            ad_second=None,
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

        self.ad_first = ad_first
        self.ad_second = ad_second
        self.med_training = med_training
        self.email = email
        self.phone = phone
        self.know_nbr = know_nbr
        self.key_nbr = key_nbr
        self.news_ltr = news_ltr
        self.contact = contact
        self.validated = False

    def validate_data(self) -> bool:
        """
        Checks the types of all data to make sure required data is input and optional data is no wrong type
        :return:
        """
        # Required data must be the correct type
        if not isinstance(self.adults, int): return False
        if not isinstance(self.children, int): return False
        if not isinstance(self.pets, bool): return False
        if not isinstance(self.dogs, bool): return False
        if not isinstance(self.crit_meds, bool): return False
        if not isinstance(self.ref_meds, bool): return False
        if not isinstance(self.special_needs, bool): return False
        if not isinstance(self.gas_tank, bool): return False
        if not isinstance(self.gas_line, bool): return False
        if not isinstance(self.ad_first, str): return False
        if not isinstance(self.ad_second, str): return False
        # Optional data can be either null or the correct type
        if not (isinstance(self.phone, str) or not self.phone): return False
        if not (isinstance(self.email, str) or not self.email): return False
        if not (isinstance(self.med_training, bool) or not self.med_training): return False
        if not (isinstance(self.know_nbr, bool) or not self.know_nbr): return False
        if not (isinstance(self.key_nbr, bool) or not self.key_nbr): return False
        if not (isinstance(self.news_ltr, bool) or not self.news_ltr): return False
        if not (isinstance(self.contact, bool) or not self.contact): return False
        # If all checks pass
        return True

    def to_dataframe(self) -> pd.DataFrame:
        """
        Creates a panda's dataframe row of this object
        :return: dataframe row
        """
        if not self.validate_data():
            print("Error: Household object not valid")
            return None
        dict = {
            "adults":        self.adults,
            "children":      self.children,
            "pets":          self.pets,
            "dogs":          self.dogs,
            "crit_meds":     self.crit_meds,
            "ref_meds":      self.ref_meds,
            "special_needs": self.special_needs,
            "gas_tank":      self.gas_tank,
            "gas_line":      self.gas_line,
            "ad_first":      self.ad_first,
            "ad_second":     self.ad_second,
            "med_training":  self.med_training,
            "email":         self.email,
            "phone":         self.phone,
            "know_nbr":      self.know_nbr,
            "key_nbr":       self.key_nbr,
            "news_ltr":      self.news_ltr,
            "contact":       self.contact,
        }
        df = pd.DataFrame([dict])
        return df

def main():
    """
    This function is just used for dev testing
    """

    print("Running in dev mode")

    # test one household
    hh = Household(
        adults=3,
        children=3,
        pets=True,
        dogs=True,
        crit_meds=False,
        ref_meds=False,
        special_needs=True,
        gas_tank=True,
        gas_line=False,
        ad_first="742 Evergreen Terrace",
        ad_second="Springfield, OR 55555",
        med_training=False,
        email="el_barto@hotmail.com",
        phone="5035551234",
        know_nbr=True,
        key_nbr=False,
        news_ltr=None,
        contact=False
    )
    print(f"Is valid? {hh.validate_data()}")

    print(hh.to_dataframe().to_string())

    # test several households

    hh1 = Household(adults=2, children=0, pets=False, dogs=False, crit_meds=True,
                    ref_meds=False, special_needs=False, gas_tank=False, gas_line=True,
                    ad_first="123 Maple St", ad_second="Portland, OR 97201",
                    med_training=True, email="alice@example.com", phone="5031112222",
                    know_nbr=False, key_nbr=True, news_ltr=True, contact=False)

    hh2 = Household(adults=4, children=2, pets=True, dogs=False, crit_meds=False,
                    ref_meds=True, special_needs=True, gas_tank=True, gas_line=False,
                    ad_first="456 Oak Ave", ad_second="Eugene, OR 97401",
                    med_training=False, email="bob@example.org", phone="5033334444",
                    know_nbr=True, key_nbr=False, news_ltr=False, contact=False)

    hh3 = Household(adults=1, children=3, pets=True, dogs=True, crit_meds=False,
                    ref_meds=False, special_needs=False, gas_tank=False, gas_line=False,
                    ad_first="789 Pine Rd", ad_second="Salem, OR 97301",
                    med_training=False, email="carol@example.net", phone="5035556666",
                    know_nbr=False, key_nbr=False, news_ltr=True, contact=False)

    hh4 = Household(adults=3, children=1, pets=False, dogs=False, crit_meds=True,
                    ref_meds=True, special_needs=False, gas_tank=True, gas_line=True,
                    ad_first="321 Birch Blvd", ad_second="Bend, OR 97701",
                    med_training=True, email="dave@example.com", phone="5037778888",
                    know_nbr=True, key_nbr=True, news_ltr=None, contact=False)

    hh5 = Household(adults=5, children=0, pets=True, dogs=True, crit_meds=False,
                    ref_meds=False, special_needs=True, gas_tank=False, gas_line=False,
                    ad_first="654 Cedar Ln", ad_second="Gresham, OR 97030",
                    med_training=False, email="eve@example.org", phone="5039990000",
                    know_nbr=False, key_nbr=True, news_ltr=False, contact=False)

    hh6 = Household(adults=2, children=2, pets=False, dogs=False, crit_meds=False,
                    ref_meds=False, special_needs=False, gas_tank=False, gas_line=False,
                    ad_first="987 Spruce St", ad_second="Hillsboro, OR 97123",
                    med_training=False, email="frank@example.net", phone="5031113333",
                    know_nbr=True, key_nbr=False, news_ltr=True, contact=True)

    hh7 = Household(adults=3, children=4, pets=True, dogs=False, crit_meds=True,
                    ref_meds=False, special_needs=False, gas_tank=True, gas_line=False,
                    ad_first="147 Willow Way", ad_second="Medford, OR 97501",
                    med_training=True, email="grace@example.com", phone="5032224444",
                    know_nbr=False, key_nbr=False, news_ltr=None, contact=False)

    hh8 = Household(adults=1, children=0, pets=False, dogs=False, crit_meds=False,
                    ref_meds=False, special_needs=False, gas_tank=False, gas_line=False,
                    ad_first="258 Aspen Ct", ad_second="Corvallis, OR 97330",
                    med_training=False, email="henry@example.org", phone="5035557777",
                    know_nbr=False, key_nbr=False, news_ltr=False, contact=False)

    hh9 = Household(adults=4, children=3, pets=True, dogs=True, crit_meds=True,
                    ref_meds=True, special_needs=True, gas_tank=True, gas_line=True,
                    ad_first="369 Redwood Dr", ad_second="Albany, OR 97321",
                    med_training=True, email="iris@example.net", phone="5038889999",
                    know_nbr=True, key_nbr=True, news_ltr=True, contact=False)

    hh10 = Household(adults=2, children=1, pets=False, dogs=False, crit_meds=False,
                     ref_meds=False, special_needs=False, gas_tank=False, gas_line=False,
                     ad_first="159 Cypress Pl", ad_second="Lake Oswego, OR 97035",
                     med_training=False, email="jack@example.com", phone="5034445555",
                     know_nbr=False, key_nbr=False, news_ltr=False, contact=None)

    dataframes = []
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
