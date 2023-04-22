import React from 'react';
import './ReplayItem.css'

function ReplayItem(props) {
    return (
        <div className='replay-item'>
            <img height='30px' style={{margin:0}}src={props.usrImg}></img> 
            <div className='replay-header'>
            <p style={{alignSelf:'flex-start',margin:0,borderBottom:'2px solid rgb(174, 174, 174)'}}><b>{props.usrName}</b></p>
            <div className='replay-content'>{props.content}</div>
           </div>
         

        </div>
    );
}

export default ReplayItem;
