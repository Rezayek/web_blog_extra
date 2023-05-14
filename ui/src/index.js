import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import Main from "./Main/main"
import { BrowserRouter } from "react-router-dom";
import ProfileNav from "./Profile/ProfileNav/ProfileNav";
import Post  from './PostComponent/Post';
import img from './logo192.png'
import Item from './CommentItemComponent/Item'
import logo from './logo192.png'
import Home from "./Home/Home";
import Profile from "./Profile/Profile";
import SignIn from "./SignIn/SignIn";
import SignUp from "./SignUp/SignUp";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BrowserRouter>
<Post usrImg={logo} usrName='Khalil ben romdhane' delay='1h'content="Hello blog's extra community !"/>
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
