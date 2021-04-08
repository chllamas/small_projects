# main.py
#   main runner of the program
#
# requirements, according to Google Account Help forum 
# post on Strong Password Security:
#   8+ characters (weak, but passable)
#   12+ characters (good)
#   max 64 characters
#   no related words
#   at least 1 lowercase
#   at least 1 uppercase
#   at least 1 number
#   at least 1 symbol  ! @ # $ % ^ & * . _
#
import random
import re

NEW_PASSWORD_PROMPT = """
Password Requirements:
* 8-64 characters
* At least 1 lowercase letter
* At least 1 uppercase letter
* At least 1 digit [0-9]
* At least 1 symbol [! @ # $ % ^ & * . _]
"""

MISSED_CHECK_PROMPTS = [
    "Password must be between 8-64 characters!",
    "Password needs at least 1 lowercase character.",
    "Password needs at least 1 uppercase character.",
    "Password needs at least 1 numeric character.",
    "Password needs at least 1 valid symbol."
]

# passwordCheck
#   checks given password string for strength and returns array with:
#   [0] Passed length test
#   [1] Passed lowercase test
#   [2] Passed uppercase test
#   [3] Passed number test
#   [4] Passed symbol test
def passwordCheck(password):
    arr = [True, True, True, True, True]
    uppercasePattern = '(?=.*[A-Z])'
    lowercasePattern = '(?=.*[a-z])'
    numberPattern = '(?=.*\d)'
    symbolPattern = '(?=.*[!,@,#,$,%,^,&,*,.,_])'
    if len(password) < 8 or len(password) > 64:
        arr[0] = False
    if not re.search(lowercasePattern, password):
        arr[1] = False
    if not re.search(uppercasePattern, password):
        arr[2] = False
    if not re.search(numberPattern, password):
        arr[3] = False
    if not re.search(symbolPattern, password):
        arr[4] = False
    return arr

while True:
    print(NEW_PASSWORD_PROMPT)
    userInput = input("Enter a new password: ")
    arr = passwordCheck(userInput)
    failed = False
    for x in range(len(arr)):
        if not arr[x]:
            failed = True
            print(MISSED_CHECK_PROMPTS[x])
    if not failed:
        print("Success: New password saved")
        break