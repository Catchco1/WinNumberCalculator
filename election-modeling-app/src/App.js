import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import './App.css';

function App() {
  const [plotData, setPlotData] = useState(null);
  const [inputData, setInputData] = useState({
    years: [],
    state: "",
    district: "",
    office: "",
  });

  const fetchPlotData = async () => {
    try {
      const response = await fetch(`/graph`,{method: 'POST', 
      headers: { 'Content-Type': 'application/json',},
      body: JSON.stringify(inputData) // body data type must match "Content-Type" header
    });
      const data = await response.json();
      setPlotData(data);
    } catch (error) {
      console.error('Error fetching plot data:', error);
    }
  };

  const handleInputChange = (e) => {
    console.log(e);
    if (Array.isArray(e)) {
      let temp = [];
      for (let i = 0; i < e.length; i++) {
        const { name, value } = e[i];
        temp.push(value)
        if (name === 'years') {
          setInputData({
            ...inputData,
            [name]: temp
          });
        }
      }
    }
    else {
      const { name, value } = e;
      setInputData({
        ...inputData,
        [name]: value
      });
    }
  };

  const yearOptions = [
    { value: '2018', label: '2018', name: 'years' },
    { value: '2020', label: '2020', name: 'years' },
    { value: '2022', label: '2022', name: 'years' }
  ]

  const stateOptions = [
    { value: 'WV', label: 'West Virginia', name: 'state' }
  ]

  const officeOptions = [
    { value: 'HOUSE OF DELEGATES', label: 'House of Delegates', name: 'office'}
  ]

  const districtOptions = [
    { value: '88', label: '88', name: 'district'}
  ]

  const animatedComponents = makeAnimated();

  return (
    <div className="App">
      <h1>Plotly React App</h1>
      Filter Option : {JSON.stringify(inputData)}
      <div>
        <Select
          closeMenuOnSelect={false}
          components={animatedComponents}
          isMulti
          options={yearOptions}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <Select
          closeMenuOnSelect={true}
          components={animatedComponents}
          options={stateOptions}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <Select
          closeMenuOnSelect={true}
          components={animatedComponents}
          options={officeOptions}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <Select
          closeMenuOnSelect={true}
          components={animatedComponents}
          options={districtOptions}
          onChange={handleInputChange}
        />
      </div>
      <button onClick={fetchPlotData}>Fetch Graph</button>
      {plotData && (
        <div>
          <h2>Graph</h2>
          <Plot
            data={plotData.data}
            layout={plotData.layout}
            config={{ responsive: true }}
            style={{ width: '100%', height: '1000px' }}
          />
        </div>
      )}
    </div>
  );
};

export default App;