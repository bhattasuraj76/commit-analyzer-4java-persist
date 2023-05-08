from enum import Enum


class Pattern(str, Enum):
    # Define useful regular patterns
    TEST_FILENAME = "^.*Test.java$"
    REMOVED_TEST_ANNOTATION = "- + @(.*)Test"
    REMOVED_TEST_FUNCTION_PROTOTYPE = "-[ /t]*(public|private|protected) ([a-zA-Z0-9<>._?, ]+) +test([a-zA-Z0-9_]+)" \
                                      " *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{"
    REFACTORED_TEST_FUNCTION_PROTOTYPE = "-[ /t]*(public|private|protected) ([a-zA-Z0-9<>._?, ]+) +test([a-zA-Z0-9_]+)" \
                                         " *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{([- \n]*)" \
                                         "\\+"
    ADDED_TEST_FUNCTION_PROTOTYPE = "\\+[ /t]*(public|private|protected) ([a-zA-Z0-9<>._?, ]+) +test([a-zA-Z0-9_]+)" \
                                    " *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{"
    REMOVED_ASSERT_FUNCTION_PROTOTYPE = "-[ /t]*assert([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\)"
    FUNCTION_NAME_AND_SIGNATURE = "([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\)"
    FUNCTION_NAME = "([a-zA-Z0-9_]+) *\\("
    FUNCTION_ARGUMENTS = "\\(.*\\)"



"\\+[ /t]*(public|private|protected) ([a-zA-Z0-9<>._?, ]+) +test([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{"