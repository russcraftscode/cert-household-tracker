"""
Author: Russell Johnson
Date 22 Nov 2025
SER416 Final Project
This library handles prompting the user for responses and ensuring those responses are properly formated
"""
import os


def clear_screen():
    """Clears the console output. Should work on win and mac/unix/linx"""
    # Windows systems
    print("Note: Attempting to clear screen. Please use a standard terminal emulator.")
    if os.name == 'nt':
        _ = os.system('cls')
    # Unix-like systems such as Linux or macOS
    else:
        _ = os.system('clear')


def line_split(text, max_length):
    """
    Splits text into given length lines while trying not to cut words in half
    :param text: text to split
    :param max_length: max length of a line
    :return: list of lines of split text
    """

    # Make new lines of a fixed length until there is not enough text to fill a lone
    lines = []
    remaining_text = text
    while len(remaining_text) > max_length:
        split_point = max_length
        # Start at the max length and seek back until a space is found
        while not remaining_text[split_point].isspace():
            split_point -= 1
            # If there is not a convent space to split the line then just split a word
            if split_point == 0:
                split_point = max_length
                break # Halt trying to find a space because we have used up the entire string
        # Create new line with text up to split point
        lines.append(remaining_text[:split_point])
        # Remove used text
        remaining_text = remaining_text[split_point:]
    # Make a final line with any remaining text
    lines.append(remaining_text)
    return lines


def display_table(df):
    # TODO: I might need the ability to display a table and integrate that into the user prompt
    pass


def display_menu(query, options, row_max, header=None):
    """
    Displays a question for the user with pre-defined response choices
    :param query: question to be ask
    :param options: list of options for the user
    :param row_max: horizontal size limitation
    :param header: optional line above question
    :return:
    """
    #clear_screen()
    max_l = row_max - 4  # max size of content in a row
    dash_row_list = ['-' for i in range(row_max)]
    dash_row = ''.join(pair for pair in dash_row_list)
    blank_row_list = [' ' for i in range(row_max - 2)]
    blank_row = ''.join(pair for pair in blank_row_list)
    blank_row = '|' + blank_row + '|'

    # display menu
    print(dash_row)
    # display the header if there is one
    if header:
        print(f"| {header:<{max_l}} |")
        print(blank_row)
    # display the query to the user
    question_lines = line_split(query, max_l)
    for line in question_lines:
        print(f"| {line:<{max_l}} |")
    print(dash_row)

    # print the options
    max_l -= 4  # cut the length of the display by 4 to allow for option numbering
    for i, option in enumerate(options):
        chunks = [option[i:i + max_l] for i in range(0, len(option), max_l)]
        # print the 1st line of the option
        print(f"| {i + 1} - {chunks[0]:<{max_l}} |")
        # print any additional lines
        for j in range(1, len(chunks)):
            print(f"|     {chunks[j]:<{max_l}} |")
    print(dash_row)

    print("Enter your selection number:")


def display_text_input(query, row_max, header=None):
    """
    Displays a question for the user with open ended responses
    :param query: question to be ask
    :param row_max: horizontal size limitation
    :param header: optional line above question
    :return:
    """
    max_l = row_max - 4  # max size of content in a row
    dash_row_list = ['-' for i in range(row_max)]
    dash_row = ''.join(pair for pair in dash_row_list)
    blank_row_list = [' ' for i in range(row_max - 2)]
    blank_row = ''.join(pair for pair in blank_row_list)
    blank_row = '|' + blank_row + '|'

    # display menu
    print(dash_row)
    # display the header if there is one
    if header:
        print(f"| {header:<{max_l}} |")
        print(blank_row)
    # display the query to the user
    question_lines = line_split(query, max_l)
    for line in question_lines:
        print(f"| {line:<{max_l}} |")
    print(dash_row)


def display_yes_no(query, row_max, header=None):
    """
    Displays a question for the user with a yes or no question
    :param query: string of question to ask user
    :param row_max: horizontal size limitation
    :param header: optional line above question
    :return:
    """
    max_l = row_max - 4  # max size of content in a row
    dash_row_list = ['-' for i in range(row_max)]
    dash_row = ''.join(pair for pair in dash_row_list)
    blank_row_list = [' ' for i in range(row_max - 2)]
    blank_row = ''.join(pair for pair in blank_row_list)
    blank_row = '|' + blank_row + '|'

    # display menu
    print(dash_row)
    # display the header if there is one
    if header:
        print(f"| {header:<{max_l}} |")
        print(blank_row)
    # display the query to the user
    question_lines = line_split(query, max_l)
    for line in question_lines:
        print(f"| {line:<{max_l}} |")
    print(dash_row)

    print("Make selection: <yes/no>")


def prompt_user(query, user_options=None, input_format=None, input_length=None, row_limit=60, header=None, required=True, table=None):
    """
    Prompts the user for input. Chooses the appropriate display type for the question
    :param query:  to ask the user
    :param user_options: list of options that the user may pick from (optional)
    :param input_format: optional constraint on user response ["y/n", "numeric", "int"]
    :param input_length: optional constraint requiring user to respond with that many characters
    :param row_limit: row length of the display. Defaults to 60 chars
    :param header: optional line to display above the question
    :param required: is the user required to give an answer. Defaults to true
    :return: the response of the user. Type will be determined by 'format' parameter. Defaults to string
    """
    # TODO: add format checkers for email, phone
    clear_screen()
    if table:
        display_table(table)
    # Repeat question loop until user responds appropriately
    while True:
        # Prompt the user with the correct display type
        if user_options:  # if there is a limited list of responses, display a menu
            display_menu(query, options=user_options, row_max=row_limit, header=header)
        else:
            if input_format == "y/n":  # if asking a true false question
                display_yes_no(query, row_max=row_limit, header=header)
            else:  # asking a free-form question
                display_text_input(query, row_max=row_limit, header=header)

        # Check response acceptability & strip out any lead/trailing whitespace
        user_response = input().strip()
        # Non-required questions may be blank
        if not required and user_response == "":
            return None
        # required questions cannot be blank
        if user_response == "":
            clear_screen()
            print("This is a required question.")
            continue
        # if response is not the proper length
        if len(user_response) != input_length and input_length:
            print(f"Response must be {input_length} characters long.")
            continue
        # int format questions must be answered with a integer with no symbols
        if input_format == "int":
            if user_response.isdigit():
                # Return the properly formatted response as an int value
                return int(user_response)
            else:
                clear_screen()
                print("Please respond with digits only. No letters, commas, or other symbols.")
                continue
        # int format questions must be answered with just numbers
        if input_format == "numeric":
            if user_response.isdigit():
                # Return the properly formatted response as an int value
                return user_response
            else:
                clear_screen()
                print("Please respond with digits only. No dashes, commas, or other symbols.")
                continue
        # Yes/No questions must have a response that either starts with a 'y' or a 'n'. Case does not matter
        if input_format == "y/n":
            if len(user_response) > 0:  # check to make sure the user input at least one character
                if user_response[0].lower() == 'y':
                    return True
                elif user_response[0].lower() == 'n':
                    return False
                else:
                    clear_screen()
                    print("Please respond with \"yes\" or \"no\" only. No other letters")
                    continue
        # Menu questions must have a response that matches an available option
        if user_options:
            if user_response.isdigit():
                sel_number = int(user_response)
                if sel_number > 0 and sel_number <= len(user_options):
                    return sel_number
            clear_screen()
            print("Please enter only the number of your selection with no other input")
            continue
        # Any remaining questions are free-form response, so just return the input
        return user_response


def main():
    """
    This function is just used for dev testing
    """
    print("Running in dev mode")

    test_header = "This is question 1"
    test_question = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut"+
                     " labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco"+
                     " laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in "+
                     "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat"+
                     " non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

    test_options = ["alpha", "beta", "gamma"]

    line_split("abc", 2)

    prompt_user(test_question, user_options=test_options, header="Required question", row_limit=80)
    prompt_user(test_question, user_options=test_options, header=test_header, required=False)
    prompt_user(test_question, user_options=test_options, required=False, row_limit=40)
    prompt_user(test_question, required=False)
    prompt_user(test_question, input_format="y/n", required=False)
    prompt_user(test_question, header="Required question")


if __name__ == "__main__":
    main()
