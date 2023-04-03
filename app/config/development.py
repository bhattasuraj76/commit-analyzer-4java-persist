ENVIRONMENT = "development"

# Logging
LOG_LEVEL = "DEBUG"

# Urls
APP_URL = "http://localhost:5000"
SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/dbms-project"
)

# Secret key
SECRET_KEY = "b06e296d8489873a1e361ca0fea6b5076a1066d925eb55b389d63460d02b51d9"

# Directory to hold csv files containing testcases
CSV_FOLDER = "files"
