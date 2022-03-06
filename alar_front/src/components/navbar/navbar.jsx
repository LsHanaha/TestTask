import React from "react";
import {Link} from "react-router-dom";

import styles from "./navbar.module.css";


const performLogout = async (props) => {

  await localStorage.removeItem("token");
  props.setLoggedIn(false);
}


export const Navbar = (props) => {

  const isLogIn = localStorage.getItem("token");

  return (
    <div className={styles.main}>
      <Link
        to={"/users"}
        className={styles.otherLink}
      >
        Users
      </Link>
      <Link
        to={"/async-links"}
        className={styles.otherLink}
      >
        Async Links
      </Link>

      {isLogIn &&
        <Link to={"/"} className={styles.logout} onClick={() => performLogout(props)}>
          logout
        </Link>

      }
    </div>
  )

}
