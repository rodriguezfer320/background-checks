from app.app import create_app

if __name__ == '__main__':
    # create the app
    app = create_app()

    # initialize the app
    app.run(host='0.0.0.0', port='5000')