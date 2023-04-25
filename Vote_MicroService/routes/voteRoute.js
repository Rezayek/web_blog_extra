const express=require('express')
const router =express.Router()
  router.post('/up',(req,res)=>{
    res.send('up vote');
    
  }).post('/down',(req,res)=>{

    res.send('down vote')
  })


module.exports=router