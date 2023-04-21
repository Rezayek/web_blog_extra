import React, { useState } from "react";
import "./Comment.css";
import { AiOutlineClose } from "react-icons/ai";
import { BsFillSendFill } from "react-icons/bs";
import Item from "../CommentItemComponent/Item";
function Comment(props) {
  let testData = [
    { Usrid: 0, id: 0, usrName: "Khalil ben romdhane", content: "Nice blog !" },
    { Usrid: 1, id: 1, usrName: "Rzouga", content: "Hate that :(" },
    {Usrid: 2,id: 2,usrName: "Franck ribery",content:"Nice blog hahahahahahahahahahahahah!"},
    { Usrid: 1, id: 1, usrName: "Rzouga", content: "Hate that :(" },
    { Usrid: 1, id: 1, usrName: "Rzouga", content: "Hate that :(" },
    { Usrid: 1, id: 1, usrName: "Rzouga", content: "Hate that :(" },
    { Usrid: 1, id: 1, usrName: "Rzouga", content: "Hate that :(" },
  ];
  const [data, setData] = useState(testData);
  const [text,setText]=useState('')
  return (
    <div className="comment-section">
      <div className="comment-content">
        <div className="bar">
          <AiOutlineClose
            className="close-btn"
            onClick={() => {
              props.comment(false);
            }}
          />
        </div>

        <div className="comments">
          {data.map((item) => {
            return (
              <Item
                delay="30 min."
                usrName={item.usrName}
                id={item.id}
                content={item.content}
                Usrid={item.Usrid}
              />
            );
          })}
        </div>

        <div className="comment-box">
          <textarea
            cols={4}
            rows={5.5}
            type="text"
            className="comment-input"
            placeholder="Comment..."
            onChange={(e)=>{
              setText(e.target.value)
            }}
          />
          <BsFillSendFill className="send" onClick={()=>{

           console.log(text)
            setData([...data,{content:text,Usrid: 0, id: 0, usrName: "Khalil ben romdhane"}])
   

          }} />
        </div>
      </div>
    </div>
  );
}

export default Comment;
