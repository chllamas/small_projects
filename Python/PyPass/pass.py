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
import json
import re
import secrets # we use secrets for random password generation for security purposes
import string
import sys

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

USAGE_PROMPT = """
USAGE: pass.py [action] [args...]

ACTIONS:
    keygen
        generates a new random key according to your preferences 
        in settings
    verify [password]
        verifies if your password is strong and satisfies the 
        minimum requirements for secure passwords
    toggle-digits
        toggles digits on or off in password generator
    toggle-symbols
        toggles symbols on or off in password generator
    set-length [digit]
        sets password length for password generator **Digit must
        be between [8-64]
"""

# get the settings json and cache into settings variable
fp = open("settings.json", "r")
settings = json.load(fp)
fp.close()

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

# passwordGenerate
#   creates a randomly generated password
#   following the given settings of object
#   settings
def passwordGenerate():
    newPassword = ""
    passwordLength = settings['length']
    while passwordLength > 0:
        randomChance = secrets.randbelow(10)
        if randomChance < 6: # insert letter
            letter = secrets.choice(string.ascii_letters)
            newPassword += letter
            passwordLength -= 1
        elif randomChance < 9: # insert digit
            if settings['allowDigits']:
                newPassword += str(secrets.randbelow(10))
                passwordLength -= 1
        else: # insert symbol
            if settings['allowSymbols']:
                symbols = ["!","@","#","$","%","^","&","*",".","_"]
                newPassword += secrets.choice(symbols)
                passwordLength -= 1
    return newPassword

# updateJSON
#   updates the JSON file "settings.json" with
#   our current settings object cached in script
def updateJSON():
    fp = open("settings.json", "w")
    json.dump(settings, fp)
    fp.close()

# updateSetting
#   allows for updating a setting and updating the
#   file thereafter as well
# BIN:
#   "Length" | [8-64]
#   "AllowDigits" | [True|False]
#   "AllowSymbols" | [True|False]
def updateSetting(name, value):
    if name == "Length" and isinstance(value, int):
        if value >= 8 and value <= 64:
            settings['length'] = value
            updateJSON()
            print("Settings: Password Length: " + str(value))
        else:
            print("Settings: Invalid Range [8-64]")
    elif name == "AllowDigits" and isinstance(value, bool):
        if settings['allowDigits'] != value:
            settings['allowDigits'] = value
            updateJSON()
            print("Settings: Allow Digits: " + str(value))
    elif name == "AllowSymbols" and isinstance(value, bool):
        if settings['allowSymbols'] != value:
            settings['allowSymbols'] = value
            updateJSON()
            print("Settings: Allow Symbols: " + str(value))
    else:
        print(USAGE_PROMPT)

# TEST CASE: PASSWORD GENERATION
# print(passwordGenerate())

# TEST CASE: UPDATE SETTINGS FOR FUTURE USE
# updateSetting("AllowDigits", False)

# TEST CASE: NEW PASSWORD CREATION
# while True:
#     print(NEW_PASSWORD_PROMPT)
#     userInput = input("Enter a new password: ")
#     testCases = passwordCheck(userInput)
#     failed = False
#     for x in range(len(testCases)):
#         if not testCases[x]:
#             failed = True
#             print(MISSED_CHECK_PROMPTS[x])
#     if not failed:
#         print("Success: New password saved")
#         break

if len(sys.argv) == 1:
    print(USAGE_PROMPT)
else:
    if sys.argv[1] == "keygen":
        print(passwordGenerate())
    elif sys.argv[1] == "verify":
        if len(sys.argv) > 2:
            diagnosis = passwordCheck(sys.argv[2])
            failed = False
            for x in range(len(diagnosis)):
                if not diagnosis[x]:
                    failed = True
                    print(MISSED_CHECK_PROMPTS[x])
            if not failed:
                print("Password passes all tests")
    elif sys.argv[1] == "set-length":
        if len(sys.argv) > 2:
            try:
                updateSetting("Length", int(sys.argv[2]))
            except:
                print("Settings: INPUT ERROR: ENTER VALID INT [8-64]")
    elif sys.argv[1] == "toggle-digits":
        updateSetting("AllowDigits", not settings['allowDigits'])
    elif sys.argv[1] == "toggle-symbols":
        updateSetting("AllowSymbols", not settings['allowSymbols'])
    else:
        print(USAGE_PROMPT)
