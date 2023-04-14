import React from 'react';
import './Main.css'
import { Routes,Route } from 'react-router';
import Home from '../Home/Home';
import SignIn from '../SignIn/SignIn';
import SignUp from '../SignUp/SignUp';

function main(props) {
    return (
        <div className='main'>
            <Routes>
                <Route path='/' element={<Home/>}/>
                <Route path='/signin' element={<SignIn/>}/>
                <Route path='/signup' element={<SignUp/>}/>
            </Routes>
            
        </div>
    );
}

export default main;