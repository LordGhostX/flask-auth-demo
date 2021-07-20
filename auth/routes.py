from auth import app


@app.route("/")
def home_route():
    return "Hello World"
