from App import create_app, db
from App import models

app = create_app()

with app.app_context():
    db.create_all()
    print("tables created successfully")
