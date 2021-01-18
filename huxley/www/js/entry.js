/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import "core-js";
import React from "react";
import { BrowserHistory } from "utils/BrowserHistory";
import { BrowserRouter, Route, Switch } from "react-router-dom";
var ReactDOM = require("react-dom");

var { CurrentUserActions } = require("actions/CurrentUserActions");
var { Huxley } = require("components/Huxley");

var routes = (
  <Route path="/">
    <Huxley />
  </Route>
);

window.addEventListener("DOMContentLoaded", () => {
  ReactDOM.render(
    <BrowserRouter history={BrowserHistory}>{routes}</BrowserRouter>,
    document.getElementById("huxley-app")
  );
});

CurrentUserActions.bootstrap();
