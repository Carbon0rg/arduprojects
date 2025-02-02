host = 'http://192.168.1.40:5500/';

function linearMap(value, inMin, inMax, outMin, outMax) {
  return Math.round(
    ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin
  );
}

function calcPercentage(value, total) {
  let percentage = Math.round((value / total) * 100);
  return percentage;
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
function update_data (temperature, humidity, soil_moisture, light, temperature_set, humidity_set, soil_moisture_set, light_set){
  let temperature_span = document.getElementById('temp_display');
  let humidity_span = document.getElementById('humid_display');
  let soil_span = document.getElementById('moist_display');
  let light_span = document.getElementById('light_display');

  temperature_span.textContent = `${temperature}/${temperature_set}`;
  humidity_span.textContent = `${humidity}/${humidity_set}`;
  soil_span.textContent = `${soil_moisture}/${soil_moisture_set}`;
  light_span.textContent = `${light}/${light_set}`;
  update_needle(temperature, humidity, soil_moisture, light, temperature_set, humidity_set, soil_moisture_set, light_set);

}

function update_needle(temperature, humidity, soil_moisture, light, temperature_set, humidity_set, soil_moisture_set, light_set) {
  let temperature_needle = document.getElementById('needle1');
  let humidity_needle = document.getElementById('needle2');
  let soil_needle = document.getElementById('needle3');
  let light_needle = document.getElementById('needle4');

  let temperature_perc = linearMap(calcPercentage(temperature, temperature_set)/2, 0, 100, 0, 300);
  let humidity_perc = linearMap(calcPercentage(humidity, humidity_set)/2, 0, 100, 0, 300);
  let moisture_perc = linearMap(calcPercentage(soil_moisture, soil_moisture_set)/2, 0, 100, 0, 300);
  let light_perc = linearMap(calcPercentage(light, light_set)/2, 0, 100, 0, 300);
  
  //temperature
  
  if(temperature_perc >= 300){
    temperature_needle.style.marginLeft = `300%`;
  }else if(temperature_perc <= 0){
    temperature_needle.style.marginLeft = `0%`;
  }else{
    temperature_needle.style.marginLeft = `${temperature_perc}%`;
  }

  //humidity

  if(humidity_perc >= 300){
    humidity_needle.style.marginLeft = `300%`;
  }else if(humidity_perc <= 0){
    humidity_needle.style.marginLeft = `0%`;
  }else{
    humidity_needle.style.marginLeft = `${humidity_perc}%`;
  }
  
  //soil moisture

  if(moisture_perc >= 300){
    soil_needle.style.marginLeft = `300%`;
  }else if(moisture_perc <= 0){
    soil_needle.style.marginLeft = `0%`;
  }else{
    soil_needle.style.marginLeft = `${moisture_perc}%`;
  }

  //Light

  if(light_perc >= 300){
    light_needle.style.marginLeft = `300%`;
  }else if(light_perc <= 0){
    light_needle.style.marginLeft = `0%`;
  }else{
    light_needle.style.marginLeft = `${light_perc}%`;
  }

}


function update_alerts(data){
  let fire = data.fire;
  let fire_alert = document.getElementById("firealert");
  let intrusion = data.intrusion;
  let intrusion_alert = document.getElementById("intrusionalert");
  let gas_leak = data.gas_leak;
  let gas_leak_alert = document.getElementById("gasleak");

  if(fire != 1){
    fire_alert.style.backgroundColor = "#fa5252";
  }
  else{
    fire_alert.style.backgroundColor = "#8cfc42";
  }

  if(intrusion != 1){
    intrusion_alert.style.backgroundColor = "#fa5252";
  }
  else{
    intrusion_alert.style.backgroundColor = "#8cfc42";
  }

  if(gas_leak != 1){
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
    temperature = data.temperature;
    humidity = data.humidity;
    soil_moisture = data.soil_moisture;
    light = data.light;
    temperature_set = data.temperature_set;
    humidity_set = data.humidity_set;
    soil_moisture_set = data.soil_moisture_set;
    light_set = data.light_set;

    update_alerts(data);
    update_data(temperature, humidity, soil_moisture, light, temperature_set, humidity_set, soil_moisture_set, light_set);
}

const body = document.body;

body.addEventListener('load', request_update_data());

setInterval(request_update_data, 5000);