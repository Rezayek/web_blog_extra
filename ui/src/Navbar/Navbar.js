import React from "react";
import "./Navbar.css";
import { Link } from "react-router-dom";
import logo from './blog-log.png'

function Navbar(props) {
  return (
    <div className="nav">
        <div className="log-n"> 
            <img src={logo} className="nav-img"></img>
            <Link style={{textDecoration:'none' ,color:'black',fontSize:'xx-large'}}><h4>Blog's extra</h4></Link>
        </div>
      
      <div className="links">
          <Link  className="link"  to="/signin"><b >Sign In</b></Link>
          <Link className="link"  to="/signup"><b>Sign Up</b></Link>
          <Link className="link"  to="/about"><b>About</b></Link>
      </div>
    </div>
  );
}

export default Navbar;
