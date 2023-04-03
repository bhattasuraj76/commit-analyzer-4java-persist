import csv
from .utils import *


# Exports data to a csv file 
def export_to_csv(
    headers,
    records,
    filename,
    dir
):
    if not check_dir_exists(dir):
        create_dir(dir)

    if filename.find('.csv') == -1:
        filename += '.csv'

    filepath = dir + "/" + filename

    try:
        with open(filepath, "w", newline="") as csv_file:
            my_writer = csv.writer(csv_file, delimiter=",")

            # Write header
            my_writer.writerow(headers)

            # Write records
            my_writer.writerows(records)

        print(f"Successfully generated {filename} inside directory {dir}")
        return filename
    except Exception as e:
        raise e




