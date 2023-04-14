import React from "react";
import logo from '../logo192.png'
import './Item.css'

function Item(props) {
  return (
    <div className="comment-item">
      <div className="img-usr">
        <img className="img" src={logo}></img>
        <div className="usr-time">
          <h4 className="usr">{props.usrName}</h4>
          <p className="time">{props.delay}.</p>
        </div>
      </div>
      <div className="item-content">{props.content}</div>
    </div>
  );
}

export default Item;
