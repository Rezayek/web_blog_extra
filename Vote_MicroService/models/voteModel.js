const mongoose=require('mongoose')
const Schema=mongoose.Schema
const voteSchema=new Schema({

id:{
    type:String,
    required:True},
title:{
        type:String,
        required:True  },

})
module.exports=mongoose.model('vote',voteSchema)


