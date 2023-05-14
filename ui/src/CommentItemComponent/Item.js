import React, { useState } from "react";
import logo from '../logo192.png'
import './Item.css'
import { ImArrowUp } from "react-icons/im";
import { ImArrowDown } from "react-icons/im";
import { FaCommentDots } from "react-icons/fa";
import {Link} from 'react-router-dom'
import Replay from '../Replay/Replay'
import Replies from '../ReplayItem/ReplayItem'
import ReplayItem from "../ReplayItem/ReplayItem";


function Item(props) {
  const [reply,setReply]=useState(false)
  const [replies,setReplies]=useState(false)
  const [data,setData]=useState([{id:0,usrName:"Khalil ben romdhane",content:'hahahah'},{id:1,usrName:'Rezayek hadj souguir',content:'Loool'},{id:2,usrName:"Wael Antar",content:'Grrrrrrr'}])
  return (
    <div className="comment-item">
      <div className="img-usr">
        <img className="img" src={props.usrImg}></img>
        <div className="usr-time">
          <h4 className="usr">{props.usrName}</h4>
          <p className="time">{props.delay}.</p>
        </div>
      </div>
      <div className="item-content">{props.content}</div>
      <div className="react-section" style={{borderBottom: reply?  '2px solid rgba(43, 43, 43, 0.385)':'none'}}>
      <ImArrowUp fontSize='22px'/>
      <ImArrowDown fontSize='22px'/>
      <FaCommentDots style={{marginLeft:'10px'}} fontSize='22px'/><Link style={{textDecoration:'none',color:'black'}} onClick={()=>{
        setReply((prev)=>{return !prev})
       
      }}><b>Replay</b></Link>
      <Link style={{marginLeft:'50%',textDecoration:'none',color:'black'}} onClick={()=>{
       
        setReplies((prev)=>{return !prev})
      }}><b>Replies({data.length})</b></Link>
      </div>
  
      { reply && <Replay reply={setReply} usrImg={logo} setData={setData}/>}
      <div className="replies-section" style={{paddingTop: replies ? '10px':0,    borderTop:replies ?' 2px solid rgba(43, 43, 43, 0.385)' :'none' }}>
      {replies ? data.map((item)=>{return <ReplayItem key={item.id} 
      usrImg={logo} 
      usrName={item.usrName} 
      content={item.content}/> } ): false}
        
      </div>
     
      
    </div>
  );
}

export default Item;