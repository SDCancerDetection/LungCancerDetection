// renderer.js

const zerorpc = require("zerorpc")
let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")

let formula = document.querySelector('#formula')
let result = document.querySelector('#result')
formula.addEventListener('input', () => {
  client.invoke("hello", "hi", (error, res) => {
    if (error) {
      console.log(error)
    } else {
      result.textContent = res
    }
  })
})

formula.dispatchEvent(new Event('input'))
