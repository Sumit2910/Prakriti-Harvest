import csv
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def load_fertilizer_data(csv_file):
    data = {}
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            soil = row['soil_type'].lower()
            crop = row['crop_type'].lower()
            fertilizer = row['fertilizer']
            temperature = row['temperature_range']
            humidity = row['humidity_range']

            if soil not in data:
                data[soil] = {}
            data[soil][crop] = {
                'fertilizer': fertilizer,
                'temperature_range': temperature,
                'humidity_range': humidity
            }
    return data

fertilizer_data = load_fertilizer_data('fertilizer_data.csv')

def recommend_fertilizer(soil, crop, temperature, humidity):
    soil = soil.lower()
    crop = crop.lower()
    data = fertilizer_data.get(soil, {}).get(crop, {
        'fertilizer': "No recommendation available",
        'temperature_range': "N/A",
        'humidity_range': "N/A"
    })

    if 'N/A' not in (data['temperature_range'], data['humidity_range']):
        temp_range = [int(t) for t in data['temperature_range'].split('-')]
        humidity_range = [int(h) for h in data['humidity_range'].split('-')]

        if not (temp_range[0] <= temperature <= temp_range[1]) or not (humidity_range[0] <= humidity <= humidity_range[1]):
            data['fertilizer'] = "Conditions not optimal for this recommendation"

    return {"fertilizer": data['fertilizer'], "temperature_range": data['temperature_range'], "humidity_range": data['humidity_range']}


@app.route('/input', methods=['POST'])
def get_input():
    data = request.get_json()
    soil_type = data.get('soil_type')
    crop_type = data.get('crop_type')
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    if not all([soil_type, crop_type, temperature, humidity]):
        return jsonify({"error": "Missing required parameters"})

    try:
        temperature = float(temperature)
        humidity = float(humidity)
    except ValueError:
        return jsonify({"error": "Invalid temperature or humidity value"})

    print(f"Received soil: {soil_type}, crop: {crop_type}, temp: {temperature}, humidity: {humidity}")

    fertilizer = recommend_fertilizer(soil_type, crop_type, temperature, humidity)
    return jsonify(fertilizer)

if __name__ == '__main__':
    app.run(debug=True)