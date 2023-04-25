//requiring modules
const express=require('express')
const app=express()
const dotenv=require('dotenv')
const voteRoute=require('./routes/voteRoute')
const mongoose=require('mongoose')
//env
dotenv.config()
//connecting to data base
mongoose.connect(process.env.DB_URL)
.then(()=>{
    console.log('connected to mongo db !')})
.catch((err)=>{
    console.log(err) 
})
//middlewares
app.use(express.json())
app.use("/api",voteRoute)



//start listening
app.listen(process.env.PORT,()=>{
    console.log ("server started") 

})