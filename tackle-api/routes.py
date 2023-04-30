from config import app

@app.route('/canary')
def canary():
    return "Welcome to the Tackle Take Home Project API!"
