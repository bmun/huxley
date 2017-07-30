/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var CountryActions = {
  countriesFetched(countries) {
    Dispatcher.dispatch({
      actionType: ActionConstants.COUNTRIES_FETCHED,
      countries: countries,
    });
  },
};

module.exports = CountryActions;
