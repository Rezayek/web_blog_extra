const mongoose=require('mongoose')
const Schema=mongoose.Schema
const post=new Schema({
userName:{
    type:String,
    required:true
},
content:{
    type:String,
    required:true
},
created:{
    type:Date,
    required:true
}
}
)
module.exports=mongoose.model('Post',post)