import React from 'react';
import './Replay.css'
import {BsFillSendFill} from 'react-icons/bs'
import {IoIosClose} from 'react-icons/io'
import {AiOutlineCloseCircle} from 'react-icons/ai'
function Replay(props) {
    return (
        <div className='replay'>
            
            <textarea rows='3' placeholder='Replay...' className='replay-section'></textarea>
            <BsFillSendFill fontSize='25px'/>
        </div>
    );
}

export default Replay ;