def create_routes(app):

    @app.route('/{}/languages'.format(AUGUR_API_VERSION), methods=["GET"])
    def num_languages():
      pass
