from auth import app, db
from auth.models import User

db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
