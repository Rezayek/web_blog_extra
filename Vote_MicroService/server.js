//requiring modules
const express=require('express')
const app=express()
const dotenv=require('dotenv')
const voteRoute=require('./routes/voteRoute')
//env
dotenv.config()
//middlewares
app.use(express.json())
app.use("/api",voteRoute)




app.listen(8000,()=>{
    console.log("server started")

})