from app import create_app
from app.models.website import init_db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)