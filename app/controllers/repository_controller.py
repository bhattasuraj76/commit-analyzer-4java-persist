import json
import logging

import pandas as pd
import plotly
import plotly.express as px
from flask import request, render_template

from app import db
from app.analyzer import analyze_test_statistics
from app.models import Repository, TestCase, TestCaseType
from app.services import RepositoryService
from app.analyzer.utils import get_repo_name

logger = logging.getLogger(__name__)


class RepositoryController:
    def __init__(self):
        self.repository_service = RepositoryService()

    def analyze(self):
        try:
            req_payload = request.args
            repository = db.session.query(Repository).filter_by(url=req_payload["url"]).first()
            if repository:
                added = db.session.query(TestCase) \
                    .filter_by(repository_id=repository.id, type=TestCaseType.ADDED) \
                    .all()
                removed = db.session.query(TestCase) \
                    .filter_by(repository_id=repository.id, type=TestCaseType.REMOVED) \
                    .all()
                modified = db.session.query(TestCase) \
                    .filter_by(repository_id=repository.id, type=TestCaseType.MODIFIED) \
                    .all()
            else:
                st = analyze_test_statistics(req_payload["url"])
                added, removed, modified = st["added"], st["removed"], st["modified"]

                # Insert repository
                repository = Repository(
                    url=req_payload["url"],
                    name=get_repo_name(req_payload["url"]),
                )
                db.session.add(repository)

                # Insert test cases
                self._add_test_cases(added, repository, TestCaseType.ADDED)
                self._add_test_cases(removed, repository, TestCaseType.REMOVED)
                self._add_test_cases(modified, repository, TestCaseType.MODIFIED)

                db.session.commit()

            df = pd.DataFrame({
                'TestCases': ['Added Test Cases', 'Modified Test Cases', 'Deleted Test Cases'],
                'Count': [len(added), len(modified), len(removed)],
                'Legend': ['Added Test Cases', 'Modified Test Cases', 'Deleted Test Cases']
            })
            fig = px.bar(df, x='TestCases', y='Count', color='Legend',
                         barmode='group')
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('pages/analyze.html', graphJSON=graphJSON)
            # return jsonify({"added": len(added), "removed": len(removed), "modified": len(modified)})
        except Exception as err:
            return err.__str__()

    def _add_test_cases(self, test_cases, repository, type):
        for each in test_cases:
            test_case = TestCase(
                filename=each["filename"],
                hash=each["hash"],
                message=each["msg"],
                datetime=each["datetime"],
                type=type,
                repository=repository
            )
            db.session.add(test_case)

    def compare(self):
        return render_template('pages/compare.html')

    def compare_analyze(self):
        try:
            req_payload = request.args
            repository1 = db.session.query(Repository).filter_by(url=req_payload["url1"]).first()
            if repository1:
                added1 = db.session.query(TestCase) \
                    .filter_by(repository_id=repository1.id, type=TestCaseType.ADDED) \
                    .all()
                removed1 = db.session.query(TestCase) \
                    .filter_by(repository_id=repository1.id, type=TestCaseType.REMOVED) \
                    .all()
                modified1 = db.session.query(TestCase) \
                    .filter_by(repository_id=repository1.id, type=TestCaseType.MODIFIED) \
                    .all()
            else:
                st = analyze_test_statistics(req_payload["url1"])
                added1, removed1, modified1 = st["added"], st["removed"], st["modified"]

                # Insert repository
                repository = Repository(
                    url=req_payload["url1"],
                    name=get_repo_name(req_payload["url1"]),
                )
                db.session.add(repository)

                # Insert test cases
                self._add_test_cases(added1, repository, TestCaseType.ADDED)
                self._add_test_cases(removed1, repository, TestCaseType.REMOVED)
                self._add_test_cases(modified1, repository, TestCaseType.MODIFIED)

                db.session.commit()

            repository2 = db.session.query(Repository).filter_by(url=req_payload["url2"]).first()
            if repository2:
                added2 = db.session.query(TestCase) \
                    .filter_by(repository_id=repository2.id, type=TestCaseType.ADDED) \
                    .all()
                removed2 = db.session.query(TestCase) \
                    .filter_by(repository_id=repository2.id, type=TestCaseType.REMOVED) \
                    .all()
                modified2 = db.session.query(TestCase) \
                    .filter_by(repository_id=repository2.id, type=TestCaseType.MODIFIED) \
                    .all()
            else:
                st = analyze_test_statistics(req_payload["url2"])
                added2, removed2, modified2 = st["added"], st["removed"], st["modified"]

                # Insert repository
                repository = Repository(
                    url=req_payload["url2"],
                    name=get_repo_name(req_payload["url2"]),
                )
                db.session.add(repository)

                # Insert test cases
                self._add_test_cases(added2, repository, TestCaseType.ADDED)
                self._add_test_cases(removed2, repository, TestCaseType.REMOVED)
                self._add_test_cases(modified2, repository, TestCaseType.MODIFIED)

                db.session.commit()

            df = pd.DataFrame({
                'TestCases': ['Added Test Cases', 'Modified Test Cases', 'Deleted Test Cases', \
                              'Added Test Cases', 'Modified Test Cases', 'Deleted Test Cases'],
                'Count': [len(added1), len(modified1), len(removed1), len(added2), len(modified2), len(removed2)],
                'Legend': ['Project 1', 'Project 1', 'Project 1', \
                           'Project 2', 'Project 2', 'Project 2']
            })
            fig = px.bar(df, x='TestCases', y='Count', color='Legend',
                         barmode='group')
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('pages/compare_analyze.html', graphJSON=graphJSON)
        except Exception as err:
            return err.__str__()

    def plotly(self):
        df = pd.DataFrame({
            'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges',
                      'Bananas'],
            'Amount': [4, 1, 2, 2, 4, 5],
            'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
        })
        fig = px.bar(df, x='Fruit', y='Amount', color='City',
                     barmode='group')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('pages/plotly.html', graphJSON=graphJSON)
