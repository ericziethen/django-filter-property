#!/bin/bash

#########################################
##### START OF FUNCTION DEFINITIONS #####
#########################################
run_tester () {
    local tester_name=$1
    local tester_script=$2

    echo "### TESTING START - '$tester_script' ###"
    $tester_script
    local return_code=$?

    if [[ $return_code -eq  0 ]];
    then
        echo "   No Issues"
    else
        echo "   Issues Found"
        ERROR_FOUND="true"
        ERROR_LIST+=" $tester_name"
    fi
    echo "### TESTING END - '$tester_name' ###"
}
#######################################
##### END OF FUNCTION DEFINITIONS #####
#######################################

if [ "$1" == "postgres-travis" ];
then
    echo Argument "$1" passed, use postgresql as db
    DJANGO_SETTINGS_MODULE=django_test_proj.settings_postgres_travis
elif [ "$1" == "postgres-local" ];
then
    echo Argument "$1" passed, use postgresql as db
    DJANGO_SETTINGS_MODULE=django_test_proj.settings_postgres_local
else
    echo No Argument Passed, use sqlite as default db
    DJANGO_SETTINGS_MODULE=django_test_proj.settings
fi

echo DJANGO_SETTINGS_MODULE: "$DJANGO_SETTINGS_MODULE"
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TEST_DIR=$SCRIPT_PATH/Testing

echo SCRIPT_PATH: $SCRIPT_PATH
echo TEST_DIR: $TEST_DIR

ERROR_FOUND="false"
ERROR_LIST=''

echo "### Start Testing ###"
run_tester "Pytest"         "$TEST_DIR/RunPytest.sh"
echo "### Testing finished ###"

echo "ERROR_FOUND: '$ERROR_FOUND'"
if [ $ERROR_FOUND == "false" ];
then
    echo "!!! NO TESTING ISSUE FOUND"
    echo "exit 0"
    exit 0
else
    echo "!!! CHECK OUTPUT, SOME TESTING ISSUE FOUND WITH"
    for value in $ERROR_LIST
    do
        echo "  - $value"
    done
    echo "exit 1"
    exit 1
fi
