/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var CurrentUserActions = {
  bootstrap() {
    Dispatcher.dispatch({
      actionType: ActionConstants.BOOTSTRAP,
    });
  },

  login(user) {
    Dispatcher.dispatch({
      actionType: ActionConstants.LOGIN,
      user: user
    });
  },

  logout() {
    Dispatcher.dispatch({
      actionType: ActionConstants.LOGOUT
    });
  },


  updateSchool(school) {
    Dispatcher.dispatch({
      actionType: ActionConstants.UPDATE_SCHOOL,
      school: school
    });
  }
};

module.exports = CurrentUserActions;
