/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var DelegateActions = {
  deleteDelegate(schoolID, delegate)  {
    Dispatcher.dispatch({
      actionType: ActionConstants.DELETE_DELEGATE,
      schoolID: schoolID,
      delegate: delegate
    });
  }
};

module.exports = DelegateActions;
