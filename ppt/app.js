require("dotenv").config()

const port = process.env.PORT
const api = process.env.API_URL
const name = process.env.APP_NAME

console.log("App Name:", name)
console.log("Port:", port)
console.log("API URL:", api)