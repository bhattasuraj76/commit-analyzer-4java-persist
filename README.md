# commit-analyzer-4java-persist

This project is an extension of my previous work [commit-analyzer-4java](https://github.com/bhattasuraj76/commit-analyzer-4java). It utilizes PostgreSQL to persistently store analyzed git commit results, thereby eliminating the need for recomputations.

---

This revised version provides clearer formatting and includes a hyperlink to the previous work for easy reference.

## Getting Started

To run the project, python should be installed on your machine.
Check if it is installed or not using

```
python --version
```

If it is not installed, download and install python from https://www.python.org/downloads/


Then, setup virtual environment (optional)

```
python3 -m venv venv
source venv/bin/activate
```

Then, install the requirements:

```
pip install -r requirements.txt
```

Then, create a .env file and copy contents from .env.example in the project root:

```
mv .env.example .env
```

Then, run the application:

```
flask run --debug  --port 5001
```


**Note:**
Before proceeding, please ensure that you correctly configure the PostgreSQL database credentials in the [development.py](app/config/development.py) file. Additionally, make sure that the database is correctly set up using the SQL commands provided in the [sql.txt](/sql.txt) file.


