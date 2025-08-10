*** Settings ***
Documentation     A test suite .
Library     ../resources/lib1.py

Force Tags    Group1

*** Test Cases ***
Cleaning And Washing: Custom Wait 5
    [Tags]    tag1
    ${sleep_time}=    get random wait time
    Sleep    ${sleep_time}   seconds
    Log   Running ${TEST NAME}

Cleaning And Washing: Custom Wait 6
    ${sleep_time}=    get random wait time
    Sleep    ${sleep_time}   seconds
    Log To Console   Running ${TEST NAME}

Cleaning And Washing: Custom Wait 7
    [Tags]    kw
    Log To Console   Running ${TEST NAME}

*** Keywords ***
Some Calculation
    Evaluate    3 / 5