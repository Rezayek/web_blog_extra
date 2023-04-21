import React, { useState } from "react";
import logo from '../logo192.png'
import './Item.css'
import { ImArrowUp } from "react-icons/im";
import { ImArrowDown } from "react-icons/im";
import { FaCommentDots } from "react-icons/fa";
import {Link} from 'react-router-dom'
import Replay from '../Replay/Replay'


function Item(props) {
  const [replay,setReplay]=useState(false)
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
      <div className="react-section">
      <ImArrowUp fontSize='22px'/>
      <ImArrowDown fontSize='22px'/>
      <FaCommentDots style={{marginLeft:'10px'}} fontSize='22px'/><Link onClick={()=>{
        setReplay((prev)=>{
          return !prev
        })
      }}>Replay</Link>
      <Link style={{marginLeft:'50%'}} onClick={()=>{
        setReplay(false)
      }}>replies</Link>
      </div>
      { replay && <Replay usrImg={logo}/>}
      
    </div>
  );
}

export default Item;
