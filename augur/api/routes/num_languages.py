def create_routes(app):

    @app.route('/{}/languages'.format(AUGUR_API_VERSION), methods=["GET"])
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
