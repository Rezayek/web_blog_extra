const mongoose=require('mongoose')
const Schema=mongoose.Schema
const Vote=new Schema({

type:{
    type:String,
    required:true
},
postId:{
    type:Object

},
userId:{
    type:String
}
}
)
module.exports=mongoose.model('Vote',Vote)