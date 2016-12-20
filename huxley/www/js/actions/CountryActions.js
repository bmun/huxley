/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var CountryActions = {
  countriesFetched() {
    Dispatcher.dispatch({
      actionType: ActionConstants.COUNTRIES_FETCHED
    });
  }
};

module.exports = CountryActions;
