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
          {props.postText ? (
            <div className="post-text">{props.postText}</div>
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
              if (liked1) {
                setColor1("black");
                console.log(Color1);
                liked1 = false;
              } else {
                setColor1("gray");
                setColor2("black");
                liked1 = true;
              }
            }}
          />
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
          <FaCommentDots
            className="comment"
            style={{ fontSize: "22px" }}
            onClick={() => {
              setComment(true);
            }}
          />
        </div>
        {comment && <Comment comment={setComment} />}
      </div>
    </div>
  );
}

export default Post;
