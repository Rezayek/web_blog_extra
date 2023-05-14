import React, { useEffect, useState } from 'react';
import Post from '../PostComponent/Post'

function Profile(props) {
   const [posts,setPosts]=useState([])
    useEffect(()=>{

        fetch('http://localhost:8000/api/posts')
        .then(response => response.json())
        .then(data => { setPosts(data)
        })})
            
    return (
        <div className='profile'>
            {posts.map((item)=>{return <Post usrName={item.userName} content={item.content} id={item._id}/> })}
            
        </div>
    );
}

export default Profile;