from auth import app, db
from auth.models import User
from auth.routes import *

db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
