import React from "react";
import "./SignIn.css";
import logo from "./blog-log.png";
import signin from "./signin.jpg";
import { Link,useNavigate } from "react-router-dom";


function SignIn(props) {
  const navigate =useNavigate()
  return (
    <div className="sign-in">
      <div className="header">
      <img className='logo' src={logo} onClick={()=>{
        navigate('/')
      }}/>
        <p className="name">
          <Link to='/' style={{textDecoration:'none' ,color:'black'}}><b>Blog's extra</b></Link>
        </p>
      </div>
      <div className="container-in">
        <div className="side-in">
          <img src={signin} className="sign-img"></img>
        </div>

        <form className="signin-form">
          <p style={{ alignSelf: "center", margin: 0, fontSize: "23px" }}>
            <b>
              Welcome back to{" "}
              <span style={{ color: "rgb(16, 88, 175)" }}>Blog's extra</span> !
            </b>
          </p>
          <label className="label">Email :</label>
          <input type="text" className="input" />

          <label className="label">Password :</label>
          <input type="password" className="input" />

          <input type="submit" className="submit-btn" value="Connect" />
          <p style={{ alignSelf: "center" }}>
            {" "}
            You don't have an account ? <Link to='/signup' style={{color:'black'}}><b>register now</b></Link>{" "}
          </p>
        </form>
      </div>
    </div>
  );
}

export default SignIn;
