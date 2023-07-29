from flask import Flask
from routes.search_routes import search_routes_bp

app = Flask(__name__)

# register new api route with app
app.register_blueprint(search_routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
