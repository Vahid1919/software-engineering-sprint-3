# Contains functions used for responsive input validation, (to avoid too much code in app.py)

def missing_fields(form_result, index_list_names):
    # Used for checking if a form inputs are missing 
    # Returns an appropriate message or 1 if there are no missing fields
    message = "Please enter: "
    for i in range(len(form_result)):
        if form_result[i] == "":
            message += index_list_names[i] + ", "
    if message != "Please enter: ":
        message = message[:-2] + "."
        return message
    else:
        return 1

def length_validation(form_result, index_list_lengths, index_list_names):
    # Used for checking if a form inputs are of valid lengths
    # Returns 1 if true, else it return an appropriate message
    message = "The following are too long: "
    for i in range(len(form_result)):
        if len(form_result[i]) > index_list_lengths[i]:
            message += index_list_names[i] + ", " 
    if message != "The following are too long: ":
        message = message[:-2] + "."
        return message
    else:
        return 1


def visitor_validate(form_result):
    # Takes an array of form inputs
    # Returns a bool for validity along with a message specifying what is missing or invalid
    # Checks input length for all fields, as well as necessary fields
    # Field indexes:
    # 0 name
    # 1 city
    # 2 address
    # 3 email
    # 4 phone
    index_list_names = ["name", "city", "address", "email", "phone number"]
    index_list_lengths = [70,35,70,64,20] # based on mysql tables
    
    # Step 1: Missing fields 
    message = missing_fields(form_result, index_list_names)
    if message != 1:
        return (0, message)

    # Step 2: Length validation
    message = length_validation(form_result, index_list_lengths, index_list_names)
    if message != 1:
        return (0, message)

    return (1, "")


def place_validate(form_result):
    # Takes an array of form inputs
    # Returns a bool for validity along with a message specifying what is missing or invalid
    # Checks input length for all fields, as well as necessary fields
    # Field indexes as follows:
    # 0 pname
    # 1 phone
    # 2 address
    # 3 email
    index_list_names = ["place name", "phone number", "address", "email"]
    index_list_lengths = [70,20,70,64] # based on mysql tables
    
    # Step 1: Missing fields 
    message = missing_fields(form_result, index_list_names)
    if message != 1:
        return (0, message)

    # Step 2: Length validation
    message = length_validation(form_result, index_list_lengths, index_list_names)
    if message != 1:
        return (0, message)
    
    return (1, "")

def agent_validate(form_result):
    # Takes an array of form inputs
    # Returns a bool for validity along with a message specifying what is missing or invalid
    # Checks for necessary fields
    # Field indexes as follows:
    # 0 agent_id
    # 1 username
    # 2 password
    index_list_names = ["agent id", "username", "password"]

    # Missing fields 
    message = missing_fields(form_result, index_list_names)
    if message != 1:
        return (0, message)

    return (1, "")


def hospital_validate(form_result):
    # Takes an array of form inputs
    # Returns a bool for validity along with a message specifying what is missing or invalid
    # Checks for necessary fields
    # Field indexes as follows:
    # 0 username
    # 1 password
    index_list_names = ["username", "password"]

    # Missing fields 
    message = missing_fields(form_result, index_list_names)
    if message != 1:
        return (0, message)

    return (1, "")








