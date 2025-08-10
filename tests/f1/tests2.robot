*** Settings ***
Documentation     A test suite .
Library    ../resources/lib1.py
Default Tags      Group2

*** Test Cases ***

Group2: Custom Wait 5
    ${sleep_time}=    get random wait time
    Sleep    ${sleep_time}   seconds
    Some Calculation

Group2: Custom Wait 6
    ${sleep_time}=    get random wait time
    Sleep    ${sleep_time}   seconds
    Log To Console   Running ${TEST NAME}

Group2: Custom Wait 7
    ${sleep_time}=    get random wait time
    Sleep    ${sleep_time}   seconds
    Log To Console   Running ${TEST NAME}


*** Keywords ***
Some Calculation
    Evaluate    3 / 5