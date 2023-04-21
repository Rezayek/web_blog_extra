import React from 'react';
import './ReplayItem.css'

function ReplayItem(props) {
    return (
        <div className='replay-item'>
           <div className='replay-header'>
            <img height='30px' style={{margin:0}}src={props.usrImg}></img>
            <p style={{alignSelf:'flex-start',margin:0}}><b>{props.usrName}</b></p>
           </div>
           
           <div className='replay-content'>{props.content}</div>
        </div>
    );
}

export default ReplayItem;
