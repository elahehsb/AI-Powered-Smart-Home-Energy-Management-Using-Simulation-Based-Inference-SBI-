import React, { useState } from 'react';
import Plot from 'react-plotly.js';

const EnergyDashboard = () => {
    const [data, setData] = useState([]);
    const [cost, setCost] = useState(0);

    const fetchEnergyData = () => {
        // Fetch data from the backend API
        fetch('/api/energy_data')
            .then(response => response.json())
            .then(data => {
                setData(data.usage);
                setCost(data.cost);
            });
    };

    return (
        <div>
            <h2>Smart Home Energy Management</h2>
            <button onClick={fetchEnergyData}>Run Simulation</button>
            <Plot
                data={[
                    {
                        x: data.map((_, idx) => idx + 1),
                        y: data,
                        type: 'scatter',
                        mode: 'lines+markers',
                        marker: { color: 'blue' },
                    },
                ]}
                layout={{ title: 'Daily Energy Usage' }}
            />
            <h3>Total Cost: ${cost.toFixed(2)}</h3>
        </div>
    );
};

export default EnergyDashboard;
