import React from "react";
import { Switch, Route, BrowserRouter } from "react-router-dom";
import { Home } from 'features/home/home';
import { Users } from 'features/users/user';
import {AsyncLinks} from "features/asyncLinks/asyncLinks";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Switch>
          <Route exact path={"/"}>
            <Home />
          </Route>
          <Route path={"/users"}>
            <Users />
          </Route>
          <Route path={"/async-links"}>
            <AsyncLinks />
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
