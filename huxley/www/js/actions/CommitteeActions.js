/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var CommitteeActions = {
  committeesFetched() {
    Dispatcher.dispatch({
      actionType: ActionConstants.COMMITTEES_FETCHED
    });
  }
};

module.exports = CommitteeActions;
