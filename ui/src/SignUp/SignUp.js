import React from "react";
import "./SignUp.css";
import Blog from "./blog.png";
import logo from "./blog-log.png";
import {Link, useNavigate} from 'react-router-dom'
function SignUp(props) {
  const navigate=useNavigate()
  return (
    <div className="signup">
      <div className="header">
        <img className="logo" src={logo} onClick={()=>{
          navigate('/')
        }}/>
        <p className="name">
          <Link to='/' style={{color:'black',textDecoration:'none'}}><b>Blog's extra</b></Link>
        </p>
      </div>
      <div className="container">
        <div className="side">
          <h1 className="h1-text">SignUp for free now !</h1>
          <img src={Blog}></img>
        </div>

        <form className="signin-form">
          <p style={{ alignSelf: "center", margin: 0, fontSize: "23px" }}>
            <b>
              {" "}
              Welcome to{" "}
              <span style={{ color: "rgb(16, 88, 175)" }}>
                Blog's extra
              </span> !{" "}
            </b>
          </p>
          <label className="label">Email :</label>
          <input type="text" className="input" />

          <label className="label">Name :</label>
          <input type="text" className="input" />

          <label className="label">Password :</label>
          <input type="password" className="input" />
          <label>Upload a profile picture :</label>

          <label style={{ display: "block" }} className="label-file" for="file">
            Upload{" "}
          </label>
          <input type="file" id="file" />

          <input type="submit" className="submit-btn" value="Submit" />
        </form>
      </div>
    </div>
  );
}

export default SignUp;
