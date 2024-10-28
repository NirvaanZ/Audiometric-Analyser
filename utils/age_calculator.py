from datetime import datetime

def calculate_age(dob):
    # Parse the DOB string into a date object
    dob_date = datetime.strptime(dob, "%Y-%m-%d")
    
    # Get today's date
    today = datetime.today()
    
    # Calculate age by subtracting the year of birth from the current year
    age = today.year - dob_date.year
    
    # If the birth date has not occurred yet this year, subtract 1 from the age
    if (today.month, today.day) < (dob_date.month, dob_date.day):
        age -= 1

    return age



# print(calculate_age("1994-05-15"))




