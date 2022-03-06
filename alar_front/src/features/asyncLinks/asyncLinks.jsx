import React, {useState} from "react";
import {Navbar} from "components/navbar/navbar";
import {Button} from "semantic-ui-react";

import {getQueries} from 'services/backendQueries';

import styles from './asyncLinks.module.css';


export const AsyncLinks = (props) => {

  const [asyncResult, setAsyncResult] = useState([]);
  const [threadResult, setThreadResult] = useState([]);

  const loadAsync = async () => {
    try {
      const response = await getQueries("/async-links/asyncio");
      setAsyncResult(response.data);
    } catch (error) {
      console.log(error);
    }
  }

  const loadThread = async () => {
    try {
      const response = await getQueries("/async-links/threads");

      setThreadResult(response.data);
    } catch (error) {
      console.log(error);
    }
  }

  const createList = (data) => {
    const res = data.map(row => {
      return (
        <div className={styles.row} key={row.id}>
          <div className={styles.rowId}>"id": {row.id},</div>
          <div className={styles.rowName}>"name": {row.name}</div>
        </div>
      )
    })
    return res
  };


  return (
    <div className={styles.main}>
      <Navbar />

      <div className={styles.container}>
        <div className={styles.half_screen}>
          <Button onClick={() => loadAsync()}>
            Load Asyncio
          </Button>
          <div  className={styles.data}>
            {asyncResult &&

              <div>
                {createList(asyncResult)}
              </div>

            }
          </div>
        </div>
        {/*<div className={styles.half_screen}>*/}
        {/*  <Button onClick={() => loadThread()}>*/}
        {/*    Load Threads*/}
        {/*  </Button>*/}
        {/*  <div className={styles.data}>*/}
        {/*    {threadResult &&*/}

        {/*      <div>*/}
        {/*        {createList(threadResult)}*/}
        {/*      </div>*/}

        {/*    }*/}
        {/*  </div>*/}
        {/*</div>*/}
      </div>
      </div>
  )

}

