from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configuring the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_data.db'  # This will create vehicle_data.db in the project directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)


# Create the Vehicle model (table in the database)
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    error_code = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f'<Vehicle {self.make} {self.model}>'


# Route to test the app
@app.route('/')
def index():
    return "Welcome to the Vehicle Diagnostics API!"


# Route to add a vehicle (POST)
@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    try:
        data = request.get_json()

        # Check if data is provided
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        # Validate required fields
        required_fields = ['make', 'model', 'year', 'mileage']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create a new vehicle instance
        new_vehicle = Vehicle(
            make=data['make'],
            model=data['model'],
            year=data['year'],
            mileage=data['mileage'],
            error_code=data.get('error_code', None)
        )

        # Add the new vehicle to the session and commit
        db.session.add(new_vehicle)
        db.session.commit()

        return jsonify({'message': 'Vehicle added successfully!'}), 201

    except Exception as e:
        # Log the error and return a message
        return jsonify({'error': str(e)}), 500


# Route to fetch all vehicles (GET)
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{
        'id': vehicle.id,
        'make': vehicle.make,
        'model': vehicle.model,
        'year': vehicle.year,
        'mileage': vehicle.mileage,
        'error_code': vehicle.error_code
    } for vehicle in vehicles])


# Route to fetch a single vehicle by ID (GET)
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return jsonify({
        'id': vehicle.id,
        'make': vehicle.make,
        'model': vehicle.model,
        'year': vehicle.year,
        'mileage': vehicle.mileage,
        'error_code': vehicle.error_code
    })


# Route to update a vehicle by ID (PUT)
@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    data = request.get_json()

    vehicle.make = data.get('make', vehicle.make)
    vehicle.model = data.get('model', vehicle.model)
    vehicle.year = data.get('year', vehicle.year)
    vehicle.mileage = data.get('mileage', vehicle.mileage)
    vehicle.error_code = data.get('error_code', vehicle.error_code)

    db.session.commit()
    return jsonify({'message': 'Vehicle updated successfully!'})


# Route to delete a vehicle by ID (DELETE)
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle deleted successfully!'})


# Main driver
if __name__ == '__main__':
    app.run(debug=True)

