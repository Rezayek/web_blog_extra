import React from "react";
import "./ProfileNav.css";
import logo from "./blog-log.png";
import { AiOutlineSearch } from "react-icons/ai";
import profilePic from "../../logo192.png";
function ProfileNav(props) {
  return (
    <div className="profile-nav">
      <div className="left-logo">
        <h4
          style={{
            fontSize: "xx-large",
            alignSelf: "center",
            borderRight: "1px solid rgb(141, 141, 141)",
            paddingRight: "5px",
          }}
        >
          Blog's extra
        </h4>
        <p style={{fontSize:'20px' ,marginLeft:'5px',color:'rgb(16, 88, 175)'}}>    <b>Posts Feed</b></p>
      </div>
      <div className="search">
        <input
        placeholder="Search..."
          style={{
            width: "50%",
            height: "25px",
            borderColor: "black",
            borderRadius: "5px",
            alignSelf: "center",
            fontSize:'large'
        
          }}
          type="text"
        />
        <AiOutlineSearch style={{ alignSelf: "center" }} fontSize="35px" />
      </div>
      <div className="profile-pic-name">
        <img
          src={profilePic}
          style={{
            height: "70%",
            alignSelf: "center",
           borderRadius:'50%',
           borderColor:'gray'
          }}
        ></img>
        <h4 style={{ alignSelf: "center" }}>Khalil ben romdhane</h4>
      </div>
    </div>
  );
}

export default ProfileNav;
