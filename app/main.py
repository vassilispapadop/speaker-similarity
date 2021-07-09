#website is a python package cause of __init__.py
from website import create_app

app = create_app()

if __name__ == '__main__':
    #debug = true everytime we make a change re-runs automatically
    app.run(debug=True)