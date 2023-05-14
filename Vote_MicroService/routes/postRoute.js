const express=require('express')
const Post =require('../Models/post')
const router =express.Router()
  router.get('/posts',(req,res)=>
  {  let p=[]
   Post.find({}).then((posts)=>{
       p=posts
       res.json(p);
   })
   
  })


module.exports=router
