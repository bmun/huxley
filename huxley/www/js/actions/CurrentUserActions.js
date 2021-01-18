/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import ActionConstants from "constants/ActionConstants";
import { Dispatcher } from "dispatcher/Dispatcher";

const CurrentUserActions = {
  bootstrap() {
    Dispatcher.dispatch({
      actionType: ActionConstants.BOOTSTRAP,
    });
  },

  login(user) {
    console.log(user);
    Dispatcher.dispatch({
      actionType: ActionConstants.LOGIN,
      user: user,
    });
  },

  logout() {
    Dispatcher.dispatch({
      actionType: ActionConstants.LOGOUT,
    });
  },

  updateSchool(schoolID, delta, onError) {
    Dispatcher.dispatch({
      actionType: ActionConstants.UPDATE_SCHOOL,
      schoolID: schoolID,
      delta: delta,
      onError: onError,
    });
  },

  updateUser(userID, delta, onSuccess, onError) {
    Dispatcher.dispatch({
      actionType: ActionConstants.UPDATE_USER,
      userID: userID,
      delta: delta,
      onSuccess: onSuccess,
      onError: onError,
    });
  },
};

export { CurrentUserActions };
