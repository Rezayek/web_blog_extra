import React from 'react';
import './Replay.css'
import {BsFillSendFill} from 'react-icons/bs'
import {IoIosClose} from 'react-icons/io'
import {AiOutlineCloseCircle} from 'react-icons/ai'
function Replay(props) {
    let reply=''
    return (
        <div className='replay'>
            <textarea rows='3' placeholder='Reply...' className='replay-section' onChange={(e)=>{
              reply=e.target.value;
              console.log(reply)

            }}></textarea>
            <BsFillSendFill fontSize='25px' onClick={()=>{
                if(!reply.length==0)
                {document.querySelector('.replay-section').style.borderColor='black'
                    props.setData((prev)=>[...prev,{id:prev.length+1,content:reply}])

                }
                else
                {
                    document.querySelector('.replay-section').style.borderColor='red'
                }
                
            }}/>
        </div>
    );
}

export default Replay ;