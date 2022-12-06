def create_routes(app):

    @app.route('/{}/languages'.format(AUGUR_API_VERSION), methods=["GET"])
    def num_languages():
      num_of_languages_sql = s.sql.text("""
            SELECT COUNT ( DISTINCT programming_language ) AS "Number of Languages"
            FROM repo_labor 
            WHERE repo_id = XXXX ;
        """)
        results = pd.read_sql(num_of_languages_sql,  server.engine)
        data = results.to_json(orient="records", date_format='iso', date_unit='ms')
        return Response(response=data, status=200, mimetype="application/json")
