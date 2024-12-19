// src/renderer.js

function getData() {
    window.api.fetchData()
    .then(data => {
      console.log('Data received from Python:', data);
  
      for (i of data) {
          const todoElement = document.getElementById('elems');
          var newElem = document.createElement('p')
          newElem.innerText = `${i[0]}, ${i[1]}, ${i[2]}`
          todoElement.appendChild(newElem)
          console.log(i[0]+" data")
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Init, then getData every 2minutes
getData()
setInterval(() => {
    getData()
    print("called !")
}, 120000);

