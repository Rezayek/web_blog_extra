//requiring modules
const express=require('express')
const app=express()
const dotenv=require('dotenv')
const postRoute=require('./routes/postRoute')
const mongoose=require('mongoose')
const Post=require('./Models/post')
const Vote=require('./Models/vote')

const cors = require('cors');
const voteRoute=require("./routes/voteRoute")

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
app.use(cors())
app.use(express.json())

app.use("/api",postRoute)
app.use("/api",voteRoute)



//start listening
app.listen(process.env.PORT,()=>{
    console.log ("server started") 
})