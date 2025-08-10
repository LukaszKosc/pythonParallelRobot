*** Settings ***
Documentation     A test suite .
Library     ../resources/lib1.py

Force Tags    Group1

*** Test Cases ***
Cleaning And Washing XX Custom Wait 35
    [Tags]    tag1
    Log To Console   Running ${TEST NAME}

Cleaning And Washing: Custom Wait 36
    Log To Console   Running ${TEST NAME}

Cleaning And Washing: Custom Wait 37
    [Tags]    kw
    Log To Console   Running ${TEST NAME}

Group2: Custom Wait 35
    Log To Console   Running ${TEST NAME}

Group2: Custom Wait 36
    Log To Console   Running ${TEST NAME}

Group2: Custom Wait 37
    Log To Console   Running ${TEST NAME}

GroupXYZ a: Custom Wait 37
    Log To Console   Running ${TEST NAME}

