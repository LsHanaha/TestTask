import React from 'react';
import {Navbar} from "../../components/navbar/navbar";
import styles from './home.module.css';

export const Home = () => {

  return (
    <div>
      <Navbar />
      <div className={styles.text}>
        Select between 2 targets in top of the page
      </div>
    </div>
  )
}
