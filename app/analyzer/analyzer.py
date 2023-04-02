import logging
from copy import deepcopy

from pydriller import Repository

from . import config
from .core import (
    analyze_test_cases_removal_in_commit_file,
    analyze_test_cases_addition_in_commit_file,
)
from .utils import is_candidate_file, format_commit_datetime, get_repo_name

logger = logging.getLogger(__name__)

"""
  Analyze Java github repository and get commits with list of 
  test cases added, removed or modified the from java test 
  files 
"""


def analyze_test_statistics(repo_url):
    try:
        results = {"added": [], "removed": [], "modified": []}
        commits = Repository(
            repo_url,
            only_modifications_with_file_types=config.JAVA_FILE_EXT,
            # since=config.COMMIT_START_DATETIME, to=config.COMMIT_END_DATETIME,
            order="reverse",
        ).traverse_commits()

        for commit in commits:
            # commit_datetime = format_commit_datetime(commit.committer_date)
            commit_datetime = commit.committer_date
            commit_hash = commit.hash
            commit_msg = commit.msg
            commit_master_data = {
                "datetime": commit_datetime,
                "hash": commit_hash,
                "msg": commit_msg,
                "author_email": commit.author.name,
                "author_name": commit.author.email
            }

            # Holds all test cases across multiple modified files; helps to eliminate
            # considering moved test cases having same name
            all_added_test_cases = []
            all_removed_test_cases = []
            all_modified_test_cases = []

            for file_idx, file in enumerate(commit.modified_files):
                filename = file.filename
                # Check if file is a candidate file
                if not is_candidate_file(filename):
                    continue

                removed_test_cases_file = analyze_test_cases_removal_in_commit_file(
                    file
                )
                added_test_cases_file = analyze_test_cases_addition_in_commit_file(file)
                logger.info(added_test_cases_file)
                removed_test_cases_file = {
                    "file_index": file_idx,
                    "filename": filename,
                    **removed_test_cases_file,
                }
                added_test_cases_file = {
                    "file_index": file_idx,
                    "filename": filename,
                    **added_test_cases_file,
                }
                all_removed_test_cases.append(removed_test_cases_file)
                all_added_test_cases.append(added_test_cases_file)

            # Get only the added test cases (per file) and flatten it
            added_test_function_only = map(
                lambda x: x["added_test_cases"], all_added_test_cases
            )
            added_test_function_only = [
                item for sublist in added_test_function_only for item in sublist
            ]

            # Filter our modified test cases from added and deleted test cases
            temp_all_removed_test_cases = deepcopy(all_removed_test_cases)
            temp_all_added_test_cases = deepcopy(all_added_test_cases)
            for index, removed_test_cases_data_in_file in enumerate(
                all_removed_test_cases
            ):
                removed_test_cases_in_file = removed_test_cases_data_in_file[
                    "removed_test_cases"
                ]
                for removed_test_case in removed_test_cases_in_file:
                    # Check if test function is moved to different file in same commit
                    # becomes removed from one file and added in another file; false positive
                    if removed_test_case in added_test_function_only:
                        all_modified_test_cases.append(
                            [
                                removed_test_cases_data_in_file["filename"],
                                removed_test_case,
                            ]
                        )
                        if(removed_test_case in temp_all_removed_test_cases[index]["removed_test_cases"]):
                            temp_all_removed_test_cases[index]["removed_test_cases"].remove(
                                removed_test_case
                            )
                        # Remove the false positive from added test cases
                        for add_file_idx, added_test_cases_data_file in enumerate(
                            all_added_test_cases
                        ):
                            for added_test_case in added_test_cases_data_file[
                                "added_test_cases"
                            ]:
                                if removed_test_case == added_test_case:
                                    if(removed_test_case in temp_all_added_test_cases[add_file_idx]["added_test_cases"]):
                                        temp_all_added_test_cases[add_file_idx][
                                            "added_test_cases"
                                        ].remove(removed_test_case)
            all_removed_test_cases = temp_all_removed_test_cases
            all_added_test_cases = temp_all_added_test_cases

            # Parse removed test cases
            for (
                rm_test_case_file_data_idx,
                removed_test_cases_in_file_data,
            ) in enumerate(all_removed_test_cases):
                removed_test_cases_in_file = removed_test_cases_in_file_data[
                    "removed_test_cases"
                ]
                filename = removed_test_cases_in_file_data["filename"]

                removed_data = []
                for removed_test_case_idx_in_file, removed_test_case in enumerate(
                    removed_test_cases_in_file
                ):
                    data = {
                        "filename": filename,
                        "testcase": removed_test_case,
                    }

                    removed_data.append(data)
                results["removed"].append({**commit_master_data, "testcases_data": removed_data})

            # Parse added test cases
            for ad_test_case_file_data_idx, added_test_cases_in_file_data in enumerate(
                all_added_test_cases
            ):
                added_test_cases_in_file = added_test_cases_in_file_data[
                    "added_test_cases"
                ]
                filename = added_test_cases_in_file_data["filename"]
                added_data = []
                for added_test_case_idx_in_file, added_test_case in enumerate(
                    added_test_cases_in_file
                ):
                    data = {
                        "filename": filename,
                        "testcase": added_test_case,
                    }

                    added_data.append(data)
                results["added"].append({**commit_master_data, "testcases_data": added_data})
                

            # Parse modified test cases; prior form [[filename, testcase],....]
            modified_data = []
            for (
                md_test_case_file_data_idx,
                modified_test_cases_in_file_data,
            ) in enumerate(all_modified_test_cases):
                modified_test_case = modified_test_cases_in_file_data[1]
                filename = modified_test_cases_in_file_data[0]
                data = {
                    "filename": filename,
                    "testcase": modified_test_case,
                }
                modified_data.append(data)
            results["modified"].append({**commit_master_data, "testcases_data": modified_data})

            logger.info(
                get_repo_name(repo_url)
                + "......... Analyzing commit .........."
                + commit.hash
                + "....."
                + str(commit_datetime)
            )

        return results
    except Exception as e:
        raise e

# r = analyze_test_statistics("https://github.com/ThomasJaspers/java-junit-sample")
# print(r)