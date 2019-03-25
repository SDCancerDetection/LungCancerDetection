const zerorpc = require("zerorpc")
let client = new zerorpc.Client({ timeout: 100, heartbeatInterval: 1000000 })
client.connect("tcp://127.0.0.1:4242")

let formula = document.querySelector('#submit')
formula.addEventListener('click', () => {
  console.log("Fired click event");
  client.invoke("hello", document.getElementById("input-file").files[0].path, (error, res) => {
    if (error) {
      console.log(error)
    } else {
      console.log(res)
      let img = document.querySelector('#center-img');
      img.src = res + "?t=" + new Date().getTime();
    }
  })
})

formula.dispatchEvent(new Event('input'))
