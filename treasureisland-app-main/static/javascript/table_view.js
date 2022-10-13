
window.addEventListener('load', (event)=>{
    const lu= document.querySelector("#lastupdated");
    lu.textContent = document.lastModified;

    const cry = document.querySelector("#copyrightyear");
    cry.textContent = new Date().getFullYear();
})

// The url for the json file
const requestURL = 'https://mark30331.github.io/lesson2/sensor_data.json';

// requests (fetches) the json file
fetch(requestURL)
    .then(function (response) {
        return response.json();
    })
    .then(function (jsonObject) {
        console.table(jsonObject); // temporary checking for valid response and data parsing

        // store results in an array
        const Items = jsonObject['Items'];

        // organizes the data into cards
        for (let i = 0; i < 1; i++){
            if (Items[i]){
            let temp_info = document.createElement('section');
            let hum_info = document.createElement('section');
            let temp_para = document.createElement('p');
            let hum_para = document.createElement('p');
            temp_para.textContent = Items[i].temperature + '℉';
            hum_para.textContent = Items[i].humidity + '%';
            temp_info.appendChild(temp_para);
            hum_info.appendChild(hum_para);
            document.querySelector('div.temperature_class').appendChild(temp_info);
            document.querySelector('div.humidity_class').appendChild(hum_info);
            }
        
        else {
            console.log("error fetching data");
            }
}});