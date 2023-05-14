const express = require("express");
const router = express.Router();
const Vote = require("../Models/vote");

router.post("/up", (req, res) => {
  let postId = req.body.postId;
  let userId = req.body.userId;

  console.log(req.body)

  Vote.find({ postId: postId, userId: userId })
  .then((p) => {
    if (p.length == 0) {
      let vote = new Vote({
        type: "up",
        postId: postId,
        userId: userId,
      });
      console.log(vote)
      vote.save()
      .then(() => {
        console.log("vote saved");
        Vote.find({ postId: postId ,type:"up"})
        .then((vote) => {
          x=vote.length
          console.log(x)
          res.send(x+" up votes !");
        });
      });
    } else {


      console.log(p)
      if(p[0].type=='up')
          { res.send("Vote up already exist");}
          else
          {  Vote.updateOne({postId:postId,userId:userId,type:"down"},{postId:postId,userId:userId,type:"up"})
          .then(() => {
            Vote.find({ postId: postId ,type:"up"}).then((k)=>{
              console.log('updated')
                 
              res.send("updated ! "+k.length+" up votes");
            })
           
          })

          } 
      

 
    }
  });
});

router.post("/down", (req, res) => {
  let postId = req.body.postId;
  let userId = req.body.userId;

  console.log(req.body)

  Vote.find({ postId: postId, userId: userId })
  .then((p) => {
    if (p.length == 0) {
      let vote = new Vote({
        type: "down",
        postId: postId,
        userId: userId,
      });
      console.log(vote)
      vote.save()
      .then(() => {
        console.log("vote saved");
        Vote.find({ postId: postId ,type:"down"})
        .then((vote) => {
          x=vote.length
          console.log(x)
          res.send(x+" down votes !");
        });
      });
    } else {
      console.log(p)
      if(p[0].type=='down')
          { res.send("Vote up already exist");}
          else
          {  Vote.updateOne({postId:postId,userId:userId,type:"up"},{postId:postId,userId:userId,type:"down"})
          .then(() => {
            Vote.find({ postId: postId ,type:"down"}).then((k)=>{
              console.log('updated')
                 
              res.send("updated ! "+k.length+" down votes");
            })
           
          })

          }      
    }
  });
})

module.exports = router;
