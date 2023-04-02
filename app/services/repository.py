import json
import logging

import pandas as pd
import plotly
import plotly.express as px
from flask import request

from app import db
from app.analyzer import analyze_test_statistics
from app.models import Repository, TestCase, TestCaseType, Commit, Author
from app.analyzer.utils import get_repo_name

logger = logging.getLogger(__name__)


class RepositoryService:
    def __init__(self):
        pass

    def analyze_repository(self, url):
        added_testcases_records = []
        modified_testcases_records = []
        removed_testcases_records = []

        try:
            # Check if the repository exists i.e previously analyzed ?
            repository = self._find_repository_by_url(url)
            if repository:
                # Check if the repository has associated commits
                commits = self._get_repository_commits(repository)
                commits_id = tuple(map(lambda each: each.id, commits))
                if commits:
                    # Get added, modified and deleted test cases 
                    added_testcases_records = self._get_testcases(
                        commits_id, TestCaseType.ADDED
                    )
                    removed_testcases_records = self._get_testcases(
                        commits_id, TestCaseType.REMOVED
                    )
                    modified_testcases_records = self._get_testcases(
                        commits_id, TestCaseType.MODIFIED
                    )
            else:
                st = analyze_test_statistics(url)
                added, removed, modified = st["added"], st["removed"], st["modified"]
                # Insert repository
                repository = self._insert_repository(url)
                # Insert test cases
                added_testcases_records = self._insert_testcases(
                    added, repository, TestCaseType.ADDED
                )
                removed_testcases_records = self._insert_testcases(
                    removed, repository, TestCaseType.REMOVED
                )
                modified_testcases_records = self._insert_testcases(
                    modified, repository, TestCaseType.MODIFIED
                )
                db.session.commit()
            return {
                "added_testcases_records": added_testcases_records,
                "removed_testcases_records": removed_testcases_records,
                "modified_testcases_records": modified_testcases_records,
            }
        except Exception as err:
            raise err

    # Insert testcases
    def _insert_testcases(self, testcases, repository, type):
        records = []
        for each in testcases:
            author = self._find_author_by_email(each["author_email"])
            if not author:
                author = self._insert_author(
                    email=each["author_email"],
                    name=each["author_name"],
                )
            commit = self._insert_commit(
                hash=each["hash"],
                message=each["msg"],
                datetime=each["datetime"],
                repository=repository,
                author=author,
            )

            for each_testcase in each["testcases_data"]:
                testcase = self._insert_testcase(
                    filename=each_testcase["filename"],
                    testcase=each_testcase["testcase"],
                    type=type,
                    commit=commit,
                )
                records.append(testcase)

        return records

    # Insert repository
    def _insert_repository(self, repo_url):
        repository = Repository(
            url=repo_url,
            name=get_repo_name(repo_url),
        )
        db.session.add(repository)
        return repository

    # Insert author
    def _insert_author(self, name, email):
        author = Author(
            name=name,
            email=email,
        )
        db.session.add(author)

    # Insert commit
    def _insert_commit(self, hash, message, datetime, repository, author):
        commit = Commit(
            hash=hash,
            message=message,
            datetime=datetime,
            repository=repository,
            author=author,
        )
        db.session.add(commit)

    # Insert testcase
    def _insert_testcase(self, filename, testcase, type, commit):
        testcase = TestCase(
            filename=filename,
            testcase=testcase,
            type=type,
            commit=commit,
        )
        db.session.add(testcase)
        return testcase

    # Find repository by url
    def _find_repository_by_url(self, repo_url):
        repository = db.session.query(Repository).filter_by(url=repo_url).first()
        return repository

    # Find author by email address
    def _find_author_by_email(self, email):
        author = db.session.query(Author).filter_by(email=email).first()
        return author

    # Get all testcases by commit id and type
    def _get_testcases(self, commits_id, testcase_type):
        testcases = (
            db.session.query(TestCase)
            .filter(
                TestCase.commit_id.in_(commits_id),
            )
            .filter_by(type=testcase_type)
            .all()
        )
        return testcases

    # Get all repository commits
    def _get_repository_commits(self, repository):
        commits = db.session.query(Commit).filter_by(repository_id=repository.id).all()
        return commits
