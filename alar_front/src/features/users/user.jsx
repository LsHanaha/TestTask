import React, {useState, useEffect} from 'react';
import {Icon} from "semantic-ui-react";

import { Navbar } from "components/navbar/navbar";
import {LoginForm} from 'components/loginForm/loginForm';

import {getToken, getQueries, deleteQueries, postQueries, updateQueries} from 'services/backendQueries';
import {Button} from "semantic-ui-react";
import styles from './user.module.css';

export const Users = () => {

  const [isLoggedIn, setLoggedIn] = useState(false);
  const [usersList, setUsersList] = useState([]);

  const [showCreate, setShowCreate] = useState(false);
  const [showEdit, setShowEdit] = useState(false);


  const [editId, setEditId] = useState(null);
  const [changeUsername, setChangeUsername] = useState("");
  const [changeAccess, setChangeAccess] = useState("");
  const [changePassword, setChangePassword] = useState("");

  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const func = async () => {
      // debugger;
      const hasToken = await getToken();
      if (hasToken !== "")
        setLoggedIn(true);
    }
    func();
  }, [])

  useEffect(() => {
    if (!isLoggedIn)
      return;

    const func = async () => {
      const response = await getQueries("/users");
      setUsersList(response.data);
    }
    func();
  }, [isLoggedIn]);

  const createUsersList = () => {
    const newList = usersList.map(row => {
      return (
        <div className={styles.userRow} key={row.id}>
          <div>{row.id}</div>
          <div>{row.username}</div>
          <div>{row.access_right}</div>
          <Icon name="edit" size="small" className={styles.editButton}
                onClick={() => editRowStart(row.id, row.username, row.access_right)}/>
          <Icon name="delete" size="small" className={styles.removeButton}
                onClick={() => deleteRow(row.id)}/>
        </div>
      )
    });
    return newList;
  }

  const editRowStart = (rowId, username, accessRight) => {
    setChangeUsername(username);
    setChangeAccess(accessRight);
    setEditId(rowId);
    setChangePassword("");
    setShowCreate(false);
    setShowEdit(true);
  }

  const createRowStart = () => {
    setChangeUsername("");
    setChangeAccess("");
    setChangePassword("");
    setEditId(null);

    setShowCreate(true);
    setShowEdit(false);
  }

  const updateRow = async () => {
    try {
      await updateQueries('/users', {
        id: editId,
        username: changeUsername,
        access: changeAccess
      });
      const listNew = await getQueries("/users");
      setUsersList(listNew.data);
      setShowEdit(false);
    } catch (error) {
      setErrorMessage(error.message);
    }
  }

  const createRow = async () => {
    try {
      await postQueries('/users', {
        username: changeUsername,
        password: changePassword,
        access: changeAccess
      });
      const listNew = await getQueries("/users");
      setUsersList(listNew.data);
      setShowEdit(false);
    } catch (error) {
      setErrorMessage(error.message);
    }
  }

  const deleteRow = async (rowId) => {
    try {
      const response = await deleteQueries(`/users/${rowId}`);
      if (response.data.status) {
        const listNew = await getQueries("/users");
        setUsersList(listNew.data);
      }
    } catch (error) {
      setErrorMessage(error.message);
    }
  }

  return (
    <div className={styles.main}>
      <Navbar setLoggedIn={setLoggedIn} />
      <div className={styles.container}>

          {isLoggedIn &&
            <>
              <div>*Current user not shown</div>
              <div className={styles.users}>
                <div className={styles.list}>
                  <div className={styles.userRowHeader}>
                    <div>ID</div>
                    <div>Username</div>
                    <div>Access Right</div>
                    <div>&nbsp;</div>
                    <div>&nbsp;</div>
                  </div>
                  {createUsersList()}
                  <Button onClick={() => createRowStart()}>
                    Create New
                  </Button>
                </div>
                <div className={styles.userMods}>
                  {showCreate &&
                    <div>
                        <div className={styles.formName}>create</div>
                        <form action="#" className={styles.form}>
                          <div className={styles.formRow}>
                            <label htmlFor="username">Username</label>
                            <input id="username" className={styles.input} type="text" value={changeUsername}
                                   onChange={event => setChangeUsername(event.target.value)}/>
                          </div>
                          <div className={styles.formRow}>
                            <label htmlFor="password">Password</label>
                            <input id="password" className={styles.input} type="text" value={changePassword}
                                   onChange={event => setChangePassword(event.target.value)}/>
                          </div>
                          <div className={styles.formRow}>
                            <label htmlFor="access">Access rights (allowed "admin" and "user")</label>
                            <input id="access" className={styles.input} type="text" value={changeAccess}
                                   onChange={event => setChangeAccess(event.target.value)}/>
                          </div>
                          <Button onClick={() => createRow()}>
                            Create
                          </Button>
                        </form>
                    </div>
                  }
                  {showEdit &&

                      <div>
                        <div className={styles.formName}>edit</div>
                        <form action="#" className={styles.form}>
                          <div className={styles.formRow}>
                            <label htmlFor="username">Username</label>
                            <input id="username" className={styles.input} type="text" value={changeUsername}
                                   onChange={event => setChangeUsername(event.target.value)}/>
                          </div>
                          <div className={styles.formRow}>
                            <label htmlFor="access">Access rights (allowed "admin" and "user")</label>
                            <input id="access" className={styles.input} type="text" value={changeAccess}
                                   onChange={event => setChangeAccess(event.target.value)}/>
                          </div>
                          <Button onClick={() => updateRow()}>
                            Edit
                          </Button>
                        </form>
                      </div>

                  }
                  {errorMessage && <div className={styles.errorMsg}>{errorMessage}</div>}

                </div>
              </div>
            </>
          }
          {!isLoggedIn &&
            <>
              <div className={styles.helpMessage}>Default user is "admin:admin"</div>
              <div className={styles.loginForm}>
                <LoginForm setLoggedIn={setLoggedIn}/>
              </div>
            </>
          }

      </div>
    </div>
  )

}
