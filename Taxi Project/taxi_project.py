from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from djikstra import dijkstra_shortest_path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Armen2004@localhost/taxiproject'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    car = db.Column(db.String(80))


class Rides(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    driver_id = db.Column(db.Integer, nullable=False)
    start = db.Column(db.String(120), nullable=False)
    finish = db.Column(db.String(120), nullable=False)

graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('call_taxi'))
        else:
            return render_template('index.html', error="Invalid username or password")

    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmed = request.form.get('confirm_password')

        if password != confirmed:
            return render_template('signup.html', error="Passwords don't match")

        if User.query.filter_by(username=username).first():
            return render_template('signup.html', error="User already exists")

        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error="Email already exists")

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('start'))

    return render_template('signup.html')

@app.route('/call_taxi', methods=['GET', 'POST'])
def call_taxi():
    if request.method == 'POST':
        current = request.form.get('current_location')
        desired = request.form.get('destination')
        if current == desired:
            return render_template('callingTaxi.html', error="Can't call taxi from the same location")
        try:
            distance = dijkstra_shortest_path(graph, current, desired)  # <--------- do this
            taxiClass = request.form.get('taxi_class')
            price = pricing(taxiClass, distance)
            selected_driver = Driver.query.order_by(func.random()).first()
            return render_template('callingTaxi.html', success=f"{taxiClass} taxi is called. Price is {price} Your driver is {selected_driver.username}")
        except Exception as e:
            return render_template('callingTaxi.html', error="An error occurred: " + str(e))

    return render_template('callingTaxi.html')



def pricing(taxi_class, minutes):

    if minutes <= 0:
        return "Invalid time"

    pricing_structure = {
        'Casual': [
            (15, '15$'),
            (30, '25$'),
            (60, '40$'),
            (float('inf'), '50$')
        ],
        'Business': [
            (15, '20$'),
            (30, '35$'),
            (60, '50$'),
            (float('inf'), '65$')
        ],
        'Business Plus': [
            (15, '25$'),
            (30, '45$'),
            (60, '60$'),
            (float('inf'), '80$')
        ],
        'Fancy': [
            (15, '30$'),
            (30, '50$'),
            (60, '75$'),
            (float('inf'), '100$')
        ]
    }

    if taxi_class not in pricing_structure:
        return "Invalid taxi class"

    for max_minutes, price in pricing_structure[taxi_class]:
        if minutes <= max_minutes:
            return price

    return "Pricing not available" 



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
