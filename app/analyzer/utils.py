import re
import os
from datetime import datetime
from dateutil import tz
from .pattern import Pattern
from .config import DATETIME_FORMAT, COMMIT_BASE_URL


# Checks if file is a candidate file
def is_candidate_file(filename: str) -> bool:
    if filename and re.search(Pattern.TEST_FILENAME.value, filename):
        return True
    else:
        return False


# Check whether directory exists or not
def check_dir_exists(directory: str) -> bool:
    return os.path.exists(directory)


# Create a new directory
def create_dir(directory: str) -> None:
    os.makedirs(directory)


# Strip characters polluting function prototype such as '+', '-', '{' and ' '
def cleanup_function_prototype(func_prototype: str) -> str:
    return func_prototype.translate(func_prototype.maketrans("", "", "+-{")).strip()


# Strip characters polluting function name like '(', ')' and ' '
def cleanup_function_name(func_name:str) -> str:
    return func_name.translate(func_name.maketrans("", "", "()")).strip()


# Return name of function from function prototype
def get_function_name_from_prototype(function_prototype):
    func_name_search = re.search(Pattern.FUNCTION_NAME.value, function_prototype)
    func_name = cleanup_function_name(func_name_search.group())
    return func_name

# Convert datetime to local timezone
def format_commit_datetime(commit_date: datetime) -> str:
    local_datetime = commit_date.astimezone(tz.tzlocal())
    return local_datetime.strftime(DATETIME_FORMAT)


# Parse commit hash as hyperlink
def parse_commit_as_hyperlink(url: str, label: str) -> str:
    return f'=HYPERLINK("{url}", "{label}")'


# Generate full url for commit hash
def get_full_commit_url(tail: str) -> str:
    return COMMIT_BASE_URL + tail


# Get name of repository from full url
def get_repo_name(repo_url):
    if repo_url:
        return repo_url.split("/")[-1].replace(".git", "")
    else:
        return None