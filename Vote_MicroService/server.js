//requiring modules
const express=require('express')
const app=express()
const dotenv=require('dotenv')
dotenv.config()





app.listen(8000,()=>{
    console.log("server started")

})