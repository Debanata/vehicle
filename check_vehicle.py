from main import db, Vehicle, app  # Import the app from main.py

# Set up an application context
with app.app_context():
    # Fetch all vehicles
    vehicles = Vehicle.query.all()
    for vehicle in vehicles:
        print(f'ID: {vehicle.id}, Make: {vehicle.make}, Model: {vehicle.model}, Year: {vehicle.year}, Mileage: {vehicle.mileage}, Error Code: {vehicle.error_code}')
