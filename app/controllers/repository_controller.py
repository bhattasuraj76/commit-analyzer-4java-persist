import json
import logging

import pandas as pd
import plotly
import plotly.express as px
from flask import request, render_template

from app.services import RepositoryService


logger = logging.getLogger(__name__)


class RepositoryController:
    def __init__(self):
        self.repository_service = RepositoryService()

    def analyze(self):
        try:
            req_payload = request.args
            result = self.repository_service.analyze_repository(req_payload["url"])
            df = pd.DataFrame(
                {
                    "TestCases": [
                        "Added Test Cases",
                        "Modified Test Cases",
                        "Deleted Test Cases",
                    ],
                    "Count": [
                        len(result["added_testcases_records"]),
                        len(result["modified_testcases_records"]),
                        len(result["removed_testcases_records"]),
                    ],
                    "Legend": [
                        "Added Test Cases",
                        "Modified Test Cases",
                        "Deleted Test Cases",
                    ],
                }
            )
            fig = px.bar(df, x="TestCases", y="Count", color="Legend", barmode="group")
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template("pages/analyze.html", graphJSON=graphJSON)
            # return jsonify({"added": len(added), "removed": len(removed), "modified": len(modified)})
        except Exception as err:
            logger.error(err)
            return err.__str__()

    def compare(self):
        return render_template("pages/compare.html")

    def compare_analyze(self):
        try:
            req_payload = request.args
            result1 = self.repository_service.analyze_repository(req_payload["url1"])
            result2 = self.repository_service.analyze_repository(req_payload["url2"])

            df = pd.DataFrame(
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
                        "Project 1",
                        "Project 1",
                        "Project 1",
                        "Project 2",
                        "Project 2",
                        "Project 2",
                    ],
                }
            )
            fig = px.bar(df, x="TestCases", y="Count", color="Legend", barmode="group")
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template("pages/compare_analyze.html", graphJSON=graphJSON)
        except Exception as err:
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
