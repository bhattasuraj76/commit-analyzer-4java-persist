import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load env variables
load_dotenv()

# Url to cts repo
REPO_PATH = os.getenv("CTS_REPO_PATH", None)

# Branch of the cts repo to be analyzed
TARGET_BRANCH = os.getenv("CTS_TARGET_BRANCH", "master")

# Url to cts repo
COMMIT_BASE_URL = os.getenv("CTS_COMMIT_BASE_URL", "https://android.googlesource.com/platform/cts/+/")

# Directory where generated csv file is stored
OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIR", "../output")

# Valid java file extensions
JAVA_FILE_EXT = ['.java']


DEFAULT_COMMIT_RANGE_DAYS_INTERVAL = 365

# Datetime formats
DATE_FORMAT = "%m/%d/%Y"
DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"

# Commit daterange filters
cts_commit_start_date = os.getenv("CTS_COMMIT_START_DATE")
cts_commit_end_date = os.getenv("CTS_COMMIT_END_DATE")
now = datetime.now()
# Define interval in no of days to compute relative time diff
interval = int(os.getenv("CTS_COMMIT_INTERVAL", DEFAULT_COMMIT_RANGE_DAYS_INTERVAL))
COMMIT_START_DATETIME = datetime.strptime(cts_commit_start_date, DATE_FORMAT) \
    if cts_commit_start_date else (now - timedelta(days=interval))
COMMIT_END_DATETIME = datetime.strptime(cts_commit_end_date, DATE_FORMAT) \
    if cts_commit_start_date else now


# Filename of generated csv file
base_filename = os.getenv("OUTPUT_FILENAME", "cts")
date_format = "%m-%d-%Y"
parsed_cts_commit_start_date = COMMIT_START_DATETIME.strftime(date_format)
parsed_cts_commit_end_date = COMMIT_END_DATETIME.strftime(date_format)
OUTPUT_FILENAME = base_filename + '_' + parsed_cts_commit_start_date + '_' + parsed_cts_commit_end_date + '.csv'
