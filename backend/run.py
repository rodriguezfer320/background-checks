from waitress import serve
from app.app import create_app

if __name__ == '__main__':
    # create the app
    app, status = create_app()

    # initialize the app
    if status:
        serve(app, host='0.0.0.0', port='5000')
    else:
        app.run(host='0.0.0.0', port='5000')