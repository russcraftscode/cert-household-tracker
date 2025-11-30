"""
main.py
Author: Russell Johnson
Date 22 Nov 2025
SER416 Final Project
This is the main file of the CERT household tracker project.
"""


import pandas as pd
import cli_gui
import household as hh

scr_w = 60

while True:
    # main screen
    main_options = [
        "Add a household",
        "Import CSV file",
        "Export CSV file",
        "Exit"
    ]

    user_input = cli_gui.prompt_user("Main Menu", user_options=main_options)

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

