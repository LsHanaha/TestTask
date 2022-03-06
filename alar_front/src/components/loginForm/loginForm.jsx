import React, {useState} from 'react';
import {Button} from "semantic-ui-react";

import {postQueries, storeToken} from "services/backendQueries";
import styles from './loginForm.module.css';


export const LoginForm = (props) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async () => {
    try {
      const response = await postQueries('/users/login',
        {
          'username': username, 'password': password
        });
      storeToken(response.data.token);
      props.setLoggedIn(true);
    } catch (error) {
      setErrorMessage(error.message);
    }
  }

  return (
    <div>
      <form  className={styles.form} action="#">
        <div className={styles.formRow}>
          <label htmlFor="username" className={styles.label}>Username</label>
          <input id="username" className={styles.input} type="text" value={username}
                 onChange={event => setUsername(event.target.value)}/>
        </div>

        <div className={styles.formRow}>
          <label htmlFor="password" className={styles.label}>Password</label>
          <input id="password" className={styles.input} type="text" value={password}
                 onChange={event => setPassword(event.target.value)}/>
        </div>
        <div>
          <Button onClick={() => handleSubmit()}>
            Submit
          </Button>
        </div>
      </form>
      {errorMessage && <div className={styles.errorMsg}>{errorMessage}</div>}

    </div>
  )

}
