// renderer.js

const zerorpc = require("zerorpc")
let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")

let formula = document.querySelector('#button')
let result = document.querySelector('#result')
formula.addEventListener('click', () => {
  client.invoke("hello", document.querySelector('#formula').value, (error, res) => {
    if (error) {
      console.log(error)
    } else {
      console.log(res)
      //result.textContent = res
    }
  })
})

formula.dispatchEvent(new Event('input'))
