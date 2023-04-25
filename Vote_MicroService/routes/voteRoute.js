const express=require('express')
const router =express.Router()
  router.post('/up',(req,res)=>{
    res.send('up vote');
    
  })


module.exports=router