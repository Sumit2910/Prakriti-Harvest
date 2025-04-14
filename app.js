document.getElementById('fertilizer-form-element').addEventListener('submit', function(event) {
    event.preventDefault();  
    
    const soilType = document.getElementById('soil').value;
    const cropType = document.getElementById('crop').value;
    const temperature = parseFloat(document.getElementById('temperature').value);
    const humidity = parseFloat(document.getElementById('humidity').value);

   
    if (!soilType || !cropType || isNaN(temperature) || isNaN(humidity)) {
        document.getElementById('result').innerText = 'Please fill in all fields with valid values.';
        return;
    }


    const data = {
        soil_type: soilType,
        crop_type: cropType,
        temperature: temperature,
        humidity: humidity
    };


    fetch('http://127.0.0.1:5000/input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log('Response received:', response);
        
        
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        return response.json();  
    })
    .then(data => {
        console.log('JSON response:', data);
        
        
        if (data.fertilizer && data.temperature_range && data.humidity_range) {
           
            document.getElementById('result').innerText = `
                Recommended Fertilizer: ${data.fertilizer}
                \nTemperature Range: ${data.temperature_range}
                \nHumidity Range: ${data.humidity_range}`;
        } else {
            document.getElementById('result').innerText = 'Error: Incomplete data received from server.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = `An error occurred: ${error.message}`;
    });
});
