"""
Author: Russell Johnson
Date 22 Nov 2025
SER416 Final Project
This file may not make it into the final project directly.
This is to set up how a household will be generated through questions
"""

"""
The required questions are as follows: 
- the number of adults in the household, 
- the number of children, 
- are there any pets, 
- if so ask the follow up if there are any dogs, 
- does anyone in the house have critical medications,
 - if so ask the follow up if those medications need refrigeration, 
- does anyone have special needs that would require extra assistance in an evacuation, 
- does the house have a large (bigger than for a grill) propane tank
- does the house have a natural gas connection
- address of the house.
  
The optional questions are as follows: 
- household contact phone number 
- household contact email address
- does anyone in the house have any medical training
- do they know their neighbors
- do they have a neighbor's house key 
- do they want the CERT newsletter
- can CERT use their contact info for anything that is not directly related to a disaster
"""

import cli_gui

# define the max width of the screen
scr_w = 80

"""
adults = 0
children = 0
pets = False
dogs = False
crit_meds = False
ref_meds = False
special_needs = False
gas_tank = False
gas_line = False
mailing_street_number = 0 # TODO: do I want to do this as a string?
mailing_street_name = ""
mailing_city = ""
mailing_state = ""
mailing_zip = 0 # TODO: do I want to do this as a string?

phone = None
email = None
med_training = None
know_neighbors = None
neighbors_key = None
newsletter = None
contact = None
"""

req = "Required Questions"
# Ask the required questions
adults = cli_gui.prompt_user(
    "How many adults live in your household?",
    header=req, input_format="numeric", row_limit=scr_w)
children = cli_gui.prompt_user(
    "How many children live in your household?",
    header=req, input_format="numeric", row_limit=scr_w)
pets = cli_gui.prompt_user(
    "Do you have pets?",
    header=req, input_format="y/n", row_limit=scr_w)
if pets:
    dogs = cli_gui.prompt_user(
        "Do you have any dogs?",
        header=req, input_format="y/n", row_limit=scr_w)

crit_meds = cli_gui.prompt_user(
    "Does anyone in the household have critical medications?",
    header=req, input_format="y/n", row_limit=scr_w)
if crit_meds:
    ref_meds = cli_gui.prompt_user(
        "Do any of these medications need to be refrigerated?",
        header=req, input_format="y/n", row_limit=scr_w)
else:
    ref_meds = None

special_needs = cli_gui.prompt_user(
    "does anyone have special needs that would require extra assistance in an evacuation?",
    header=req, input_format="y/n", row_limit=scr_w)
gas_tank = cli_gui.prompt_user(
    "Does the house have a large propane tank? Anything larger than the standard size used in a gas grill?",
    header=req, input_format="y/n", row_limit=scr_w)
gas_line = cli_gui.prompt_user(
    "Does the house have gas hookup for cooking or gas heat?",
    header=req, input_format="y/n", row_limit=scr_w)

# optional questions
mailing_street_number = None
mailing_street_name = None
mailing_city = None
mailing_state = None
mailing_zip = None

ad_hd = "Address (optional - Enter nothing to skip"  # header for the address questions

ad_first = cli_gui.prompt_user(
    "What is the 1st line of the mailing address? Enter it as you would on an envelope, street number and then street name",
    header=ad_hd, required=False, row_limit=scr_w)
if ad_first:
    ad_second = cli_gui.prompt_user(
        "What is the 2nd line of the mailing address? Enter it as you would on an envelope, town name, then a comma, then state and zip code",
        header=ad_hd, required=False, row_limit=scr_w)
    if not ad_second:
        ad_first = None

print()
print(f"{adults=}")
print(f"{children =}")
print(f"{pets=}")
print(f"{dogs=}")
print(f"{crit_meds=}")
print(f"{ref_meds=}")
print(f"{special_needs=}")
print(f"{gas_tank=}")
print(f"{gas_line=}")

print(f"{ad_first=}")
print(f"{ad_second=}")







"""
mailing_street_number = cli_gui.prompt_user(
    "What is the street number of the house? Just the number.",
    header=ad_hd, input_format="numeric", required=False, row_limit=scr_w)
if mailing_street_number:
    mailing_street_name = cli_gui.prompt_user(
        "What is the name of the street the house is on? Just the name, no street number.",
        header=ad_hd, required=False, row_limit=scr_w)
    if mailing_street_name:
        mailing_city = cli_gui.prompt_user(
            "What is the name of the city or town the house is in?",
            header=ad_hd, required=False, row_limit=scr_w)
        if mailing_city:
            mailing_state = cli_gui.prompt_user(
                "What state is the house in?",
                header=ad_hd, required=False, row_limit=scr_w)
            if mailing_state:
                mailing_zip =   cli_gui.prompt_user(
                    "What is the name of the city or town the house is in?",
                    header=ad_hd, required=False, row_limit=scr_w)
mailing_zip = 0  # TODO: do I want to do this as a string?"""
