import json
import logging

import pandas as pd
import plotly
import plotly.express as px
from flask import jsonify, request, render_template, send_from_directory
from app.analyzer.helpers import export_to_csv
from app.services import RepositoryService
from app.analyzer.utils import get_repo_name
from app import app

logger = logging.getLogger(__name__)


class RepositoryController:
    def __init__(self):
        self.repository_service = RepositoryService()

    def analyze(self):
        try:
            req_payload = request.args
            # Parse testcases added, modified and deleted
            testcases_result = self.repository_service.analyze_repository(
                req_payload["url"]
            )
            testcases_df = pd.DataFrame(
                {
                    "TestCases": [
                        "Added Test Cases",
                        "Modified Test Cases",
                        "Deleted Test Cases",
                    ],
                    "Count": [
                        len(testcases_result["added_testcases_records"]),
                        len(testcases_result["modified_testcases_records"]),
                        len(testcases_result["removed_testcases_records"]),
                    ],
                    "Legend": [
                        "Added Test Cases",
                        "Modified Test Cases",
                        "Deleted Test Cases",
                    ],
                }
            )
            testcases_fig = px.bar(
                testcases_df,
                x="TestCases",
                y="Count",
                color="Legend",
                barmode="group",
                title="Total Testcases Added, Modified and Removed",
            )
            testcases_graphJSON = json.dumps(
                testcases_fig, cls=plotly.utils.PlotlyJSONEncoder
            )

            # Parse commits by year
            commits_result = self.repository_service.analyze_commits_by_year(
                req_payload["url"]
            )
            commits_result_md = [
                ("Total commits by year", q["count"], q["year"]) for q in commits_result
            ]
            commits_result_by_year_df = pd.DataFrame(
                commits_result_md, columns=["type", "count", "year"]
            )
            commits_by_year_fig = px.line(
                commits_result_by_year_df,
                x="year",
                y="count",
                title="Total Commits By Year",
            )
            commits_graphJSON = json.dumps(
                commits_by_year_fig, cls=plotly.utils.PlotlyJSONEncoder
            )
            return render_template(
                "pages/analyze.html",
                testcases_graphJSON=testcases_graphJSON,
                commits_graphJSON=commits_graphJSON,
            )
        except Exception as err:
            logger.error(err)
            return err.__str__()

    def compare(self):
        return render_template("pages/compare.html")

    def refresh(self):
        try:
            req_payload = request.args
            self.repository_service.delete_repository(req_payload["url"])
            return self.analyze()
        except Exception as err:
            logger.error(err)
            return err.__str__()

    def compare_analyze(self):
        try:
            req_payload = request.args
            result1 = self.repository_service.analyze_repository(req_payload["url1"])
            result2 = self.repository_service.analyze_repository(req_payload["url2"])
            project1 = get_repo_name(req_payload["url1"])
            project2 = get_repo_name(req_payload["url2"])

            testcases_df = pd.DataFrame(
                {
                    "TestCases": [
                        "Added Test Cases",
                        "Modified Test Cases",
                        "Deleted Test Cases",
                        "Added Test Cases",
                        "Modified Test Cases",
                        "Deleted Test Cases",
                    ],
                    "Count": [
                        len(result1["added_testcases_records"]),
                        len(result1["modified_testcases_records"]),
                        len(result1["removed_testcases_records"]),
                        len(result2["added_testcases_records"]),
                        len(result2["modified_testcases_records"]),
                        len(result2["removed_testcases_records"]),
                    ],
                    "Legend": [
                        project1,
                        project1,
                        project1,
                        project2,
                        project2,
                        project2,
                    ],
                }
            )
            testcases_fig = px.bar(
                testcases_df,
                x="TestCases",
                y="Count",
                color="Legend",
                barmode="group",
                title="Total Testcases Added, Modified and Removed",
            )
            testcases_graphJSON = json.dumps(
                testcases_fig, cls=plotly.utils.PlotlyJSONEncoder
            )

            # Parse commits by year
            commits_result1 = self.repository_service.analyze_commits_by_year(
                req_payload["url1"]
            )
            commits_result1_md = [
                (project1, q["count"], q["year"]) for q in commits_result1
            ]
            commits_result2 = self.repository_service.analyze_commits_by_year(
                req_payload["url2"]
            )
            commits_result2_md = [
                (project2, q["count"], q["year"]) for q in commits_result2
            ]
            commits_result_by_year = commits_result1_md + commits_result2_md
            commits_result_by_year = sorted(commits_result_by_year, key=lambda x: x[2])
            commits_result_by_year_df = pd.DataFrame(
                commits_result_by_year, columns=["project", "count", "year"]
            )
            commits_by_year_fig = px.line(
                commits_result_by_year_df,
                x="year",
                y="count",
                color="project",
                title="Total Commits By Year",
            )
            commits_graphJSON = json.dumps(
                commits_by_year_fig, cls=plotly.utils.PlotlyJSONEncoder
            )

            return render_template(
                "pages/compare_analyze.html",
                testcases_graphJSON=testcases_graphJSON,
                commits_graphJSON=commits_graphJSON,
                project1=project1,
                project2=project2,
            )
        except Exception as err:
            return err.__str__()

    def export(self):
        try:
            req_payload = request.args
            results = self.repository_service.get_all_testcases(req_payload["url"])
            filename = export_to_csv(
                headers=["hash", "filename", "testcase", "type"],
                records=results,
                filename="report",
                dir=app.config["CSV_FOLDER"],
            )
            return send_from_directory(
                "../" + app.config["CSV_FOLDER"], filename, as_attachment=True
            )
        except Exception as err:
            logger.error(err)
            return err.__str__()

    def plotly(self):
        df = pd.DataFrame(
            {
                "Fruit": [
                    "Apples",
                    "Oranges",
                    "Bananas",
                    "Apples",
                    "Oranges",
                    "Bananas",
                ],
                "Amount": [4, 1, 2, 2, 4, 5],
                "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
            }
        )
        fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template("pages/plotly.html", graphJSON=graphJSON)
