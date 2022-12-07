#SPDX-License-Identifier: MIT
import base64
import sqlalchemy as s
import pandas as pd
import json
from flask import Response

from augur.api.metrics.repo_meta import license_files
from augur.api.metrics.insight import top_insights

# from augur.api.server import transform
from augur.api.server import server

AUGUR_API_VERSION = 'api/unstable'

def create_routes(server):

    @server.app.route('/{}/languages'.format(AUGUR_API_VERSION), methods=["GET"])
    def num_languages(repo_id=None):
        num_of_languages_sql = ""
        if repo_id is None:
            num_of_languages_sql = s.sql.text("""
                SELECT repo_id, COUNT ( DISTINCT programming_language ) AS "Number of Languages"
                FROM augur_data.repo_labor
                GROUP BY repo_id;
            """)
        else:
            num_of_languages_sql = s.sql.text("""
                SELECT repo_id, COUNT ( DISTINCT programming_language ) AS "Number of Languages"
                FROM augur_data.repo_labor 
                WHERE repo_id = %d 
                GROUP BY repo_id;
            """ %(repo_id))
        results = pd.read_sql(num_of_languages_sql,  server.engine)
        data = results.to_json(orient="records", date_format='iso', date_unit='ms')
        return Response(response=data, status=200, mimetype="application/json")
