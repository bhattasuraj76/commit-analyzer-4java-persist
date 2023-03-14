import csv
from .config import OUTPUT_DIRECTORY, OUTPUT_FILENAME
from .utils import *


# Exports data as csv file in the configured output_backup_v1.0.1 directory
def export_to_csv(
    headers,
    records
):
    if not check_dir_exists(OUTPUT_DIRECTORY):
        create_dir(OUTPUT_DIRECTORY)

    filename = OUTPUT_FILENAME
    if filename.find('.csv') == -1:
        filename += '.csv'

    filepath = OUTPUT_DIRECTORY + "/" + filename

    try:
        with open(filepath, "w", newline="") as csv_file:
            my_writer = csv.writer(csv_file, delimiter=",")

            # Write header
            my_writer.writerow(headers)

            # Write records
            my_writer.writerows(records)

        print(f"Successfully generated {filename} inside directory {OUTPUT_DIRECTORY}")
    except Exception as e:
        raise e




