/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

var ActionConstants = require('../constants/ActionConstants');
var Dispatcher = require('../dispatcher/Dispatcher');

var CurrentUserActions = {
  login: function(user) {
    Dispatcher.dispatch({
      actionType: ActionConstants.LOGIN,
      user: user
    });
  },

  logout: function() {
    Dispatcher.dispatch({
      actionType: ActionConstants.LOGOUT
    });
  }
};

module.exports = CurrentUserActions;
