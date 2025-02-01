let host = 'http://192.168.1.40:5500/';

function redirect2controls(x) {
  window.location.assign(x);
}
//Humidity
const humidity_text_box = document.getElementById("humid_value");
const humid_increase = document.querySelector("#increase_humid");
const humid_decrease = document.querySelector("#decrease_humid");
humid_increase.addEventListener("click", (e) => {
  humidity_text_box.stepUp();
});
humid_decrease.addEventListener("click", (e) => {
  humidity_text_box.stepDown();
});

//Temperature
const temp_text_box = document.getElementById("temp_value");
const temp_increase = document.querySelector("#increase_temp");
const temp_decrease = document.querySelector("#decrease_temp");
temp_increase.addEventListener("click", (e) => {
  temp_text_box.stepUp();
});
temp_decrease.addEventListener("click", (e) => {
  temp_text_box.stepDown();
});

//Light

const light_text_box = document.getElementById("light_value");
const light_increase = document.querySelector("#increase_light");
const light_decrease = document.querySelector("#decrease_light");
light_increase.addEventListener("click", (e) => {
  light_text_box.stepUp();
});
light_decrease.addEventListener("click", (e) => {
  light_text_box.stepDown();
});

//soil moisture

const moisture_text_box = document.getElementById("moisture_value");
const moisture_increase = document.querySelector("#increase_moisture");
const moisture_decrease = document.querySelector("#decrease_moisture");
moisture_increase.addEventListener("click", (e) => {
  moisture_text_box.stepUp();
});
moisture_decrease.addEventListener("click", (e) => {
  moisture_text_box.stepDown();
});



//request: change values;

async function submit() {
  try {
    const url = `${host}change_data`; // Make sure server_addr is defined
    const data = {
      temperature: temp_text_box.value,
      humidity: humidity_text_box.value,
      light: light_text_box.value,
      soil_moisture: moisture_text_box.value
    };

    // Validate data
    if (!data.temperature ||!data.humidity ||!data.light ||!data.soil_moisture) {
      throw new Error('Please fill in all fields');
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      try {
        const jsonData = await response.json();
        console.log(jsonData);
        alert("Updated")
      } catch (error) {
        console.error('Error parsing JSON:', error);
      }
    } else {
      console.error(`Error: ${response.status}`);
    }
  } catch (error) {
    console.error(error);
  }
}



function linearMap(value, inMin, inMax, outMin, outMax) {
  return Math.round((value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin);
}

function calcPercentage(value, total){
  percentage = Math.round((value / total) * 100);
  return percentage;
}

function update_data (temperature_set, humidity_set, soil_moisture_set, light_set){
  let temperature_span = document.getElementById('temp_value');
  let humidity_span = document.getElementById('humid_value');
  let soil_span = document.getElementById('moisture_value');
  let light_span = document.getElementById('light_value');

  temperature_span.value = temperature_set;
  humidity_span.value = humidity_set;
  soil_span.textContent = soil_moisture_set;
  light_span.value = light_set;

}


function update_alerts(data){
  let fire = data.fire;
  let fire_alert = document.getElementById("firealert");
  let intrusion = data.intrusion;
  let intrusion_alert = document.getElementById("intrusionalert");
  let gas_leak = data.gas_leak;
  let gas_leak_alert = document.getElementById("gasleak");

  if(fire != 0){
    fire_alert.style.backgroundColor = "#fa5252";
  }
  else{
    fire_alert.style.backgroundColor = "#8cfc42";
  }

  if(intrusion != 0){
    intrusion_alert.style.backgroundColor = "#fa5252";
  }
  else{
    intrusion_alert.style.backgroundColor = "#8cfc42";
  }

  if(gas_leak != 0){
    gas_leak_alert.style.backgroundColor = "#fa5252";
  }
  else{
    gas_leak_alert.style.backgroundColor = "#8cfc42";
  }
}


async function request_update_data(){
  let response = await fetch(`${host}get_data`);
  let data = await response.json();
  console.log(data);
  temperature_set = data.temperature_set;
  humidity_set = data.humidity_set;
  soil_moisture_set = data.soil_moisture_set;
  light_set = data.light_set;

  update_data(temperature_set, humidity_set, soil_moisture_set, light_set);
  update_alerts(data);
}

const body = document.body;

body.addEventListener('load', request_update_data());