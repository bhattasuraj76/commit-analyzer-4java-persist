import app

application = app.app
application.run()
if __name__ == "__main__":
    application.debug = True
    application.port = 5001
    application.run()