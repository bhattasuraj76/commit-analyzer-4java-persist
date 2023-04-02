import re
from typing import List, Dict, Union
import logging

from pydriller.domain.commit import ModifiedFile

from .pattern import Pattern
from .utils import cleanup_function_prototype, get_function_name_from_prototype

logger = logging.getLogger(__name__)

#  Analyze commit files to detect tests cases removed
def analyze_test_cases_removal_in_commit_file(file: ModifiedFile) \
        -> Dict[str, Union[List, int, str]]:
    file_changes = file.diff
    candidate_removed_test_functions = get_removed_test_functions(file_changes)
    refactored_test_functions = get_refactored_test_functions(file_changes)
    removed_test_functions = []

    for candidate_removed_test_function in candidate_removed_test_functions:
        # Check if the removed test function is refactored test case i.e. false positive
        if candidate_removed_test_function in refactored_test_functions:
            continue

        removed_test_functions.append(candidate_removed_test_function)

    return {"removed_test_cases": removed_test_functions}


#  Analyze commit files to detect tests cases added
def analyze_test_cases_addition_in_commit_file(file: ModifiedFile) \
        -> Dict[str, Union[List, int, str]]:
    file_changes = file.diff
    added_test_functions = get_added_test_functions(file_changes)
    return {"added_test_cases": added_test_functions}


#  Get list of removed test functions from file changes
def get_removed_test_functions(file_changes: str) -> List:
    removed_testcases = []
    matched_grp = re.finditer(Pattern.REMOVED_TEST_FUNCTION_PROTOTYPE.value, file_changes)
    raw_removed_testcases = [x.group() for x in matched_grp]

    for each in raw_removed_testcases:
        function_prototype = cleanup_function_prototype(each)
        function_name = get_function_name_from_prototype(function_prototype)
        removed_testcases.append(function_name)

    return removed_testcases


#  Get refactored test functions from file changes
def get_refactored_test_functions(file_changes: str) -> List:
    removed_testcases = []
    matched_grp = re.finditer(Pattern.REFACTORED_TEST_FUNCTION_PROTOTYPE.value, file_changes)
    raw_removed_testcases = [x.group() for x in matched_grp]

    for each in raw_removed_testcases:
        function_prototype = cleanup_function_prototype(each)
        function_name = get_function_name_from_prototype(function_prototype)
        removed_testcases.append(function_name)

    return removed_testcases


#  Get added test functions from file changes
def get_added_test_functions(file_changes: str) -> List:
    added_testcases = []
    matched_grp = re.finditer(Pattern.ADDED_TEST_FUNCTION_PROTOTYPE.value, file_changes)
    raw_added_testcases = [x.group() for x in matched_grp]

    for each in raw_added_testcases:
        function_prototype = cleanup_function_prototype(each)
        function_name = get_function_name_from_prototype(function_prototype)
        added_testcases.append(function_name)

    return added_testcases


#  Get removed test assertions from file changes
def get_removed_test_assertions(file_changes: str) -> List:
    removed_assertions = []
    matched_grp = re.finditer(Pattern.REMOVED_ASSERT_FUNCTION_PROTOTYPE.value, file_changes)
    raw_removed_assertions = [x.group() for x in matched_grp]

    for each in raw_removed_assertions:
        function_prototype = cleanup_function_prototype(each)
        removed_assertions.append(function_prototype)

    return removed_assertions
