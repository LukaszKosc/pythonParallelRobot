*** Settings ***
Documentation     A test suite .
Library     ../resources/lib1.py

Force Tags      Group5

*** Test Cases ***
Painting And Wining: Custom Wait 12345
    ${time_to_sleep}=    get random wait time
    Log To Console   Running random time: ${time_to_sleep}
    Sleep     ${time_to_sleep}    seconds
    Log To Console   Running ${TEST NAME}

Painting And Wining: Custom Wait 1234
    ${time_to_sleep}=    get random wait time
    Log To Console   Running random time: ${time_to_sleep}
    Sleep     ${time_to_sleep}    seconds
    Log To Console   Running ${TEST NAME}

Painting And Wining: Custom Wait 123
    [Tags]    kw
    ${time_to_sleep}=    get random wait time
    Log To Console   Running random time: ${time_to_sleep}
    Sleep     ${time_to_sleep}    seconds
    Log To Console   Running ${TEST NAME}