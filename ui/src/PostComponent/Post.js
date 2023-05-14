import React, { useState } from "react";
import "./Post.css";
import { FaCommentDots } from "react-icons/fa";
import { ImArrowUp } from "react-icons/im";
import { ImArrowDown } from "react-icons/im";
import Comment from "../CommentComponent/Comment";

function Post(props) {
  let liked1 = false;
  let liked2 = false;
  const [Color1, setColor1] = useState("black");
  const [Color2, setColor2] = useState("black");
  const [comment, setComment] = useState(false);
  const[up,setUp]=useState(0)
  return (
    <div className="post">
      <div className="post-content">
        <div className="usrName-img">
          <img className="usrImg" src={props.usrImg}></img>

          <div className="usrName-delay">
            <h4 className="usrName">{props.usrName}</h4>
            <p className="delay">{props.delay}.</p>
          </div>
        </div>
        <div className="content">
          {props.content ? (
            <div className="post-text">{props.content}</div>
          ) : (
            ""
          )}
          {props.postImg ? (
            <img src={props.postImg} className="post-img"></img>
          ) : (
            ""
          )}
        </div>

        <div className="reaction">
          <ImArrowUp
            style={{ fontSize: "22px", color: Color1 }}
            onClick={() => {
              fetch("http://localhost:8000/api/up", {
                method: "POST",
                headers: {
                  'Content-Type': 'application/json'
                },
                body:JSON.stringify({id:props.id  }) 
              }
              
              )
              .then((res)=>{
                       res.json()
                       .then((data) => {
                        setUp(data.length)
                        if (liked1) {
                          setColor1("black");
                      
                          liked1 = false;
                        } else {
                          setColor1("gray");
                          setColor2("black");
                          liked1 = true;
                        }
                      })
              });
            }}
          />
          <p><b>70</b></p>
          <ImArrowDown
            style={{ fontSize: "22px", color: Color2 }}
            onClick={() => {
              if (liked2) {
                setColor2("black");
                liked2 = false;
              } else {
                setColor2("gray");
                setColor1("black");
                liked2 = true;
              }
            }}
          />
              <p><b>0</b></p>
          <FaCommentDots
            className="comment"
            style={{ fontSize: "22px" }}
            onClick={() => {
              setComment(true);
            }}
            
          />
              <p><b>10</b></p>
        </div>
        {comment && <Comment comment={setComment} />}
      </div>
    </div>
  );
}

export default Post;
