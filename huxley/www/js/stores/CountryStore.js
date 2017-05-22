/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var CountryActions = require('actions/CountryActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');


var _countries = {};

class CountryStore extends Store {
  getCountries() {
    if (Object.keys(_countries).length) {
      return _countries;
    }

    ServerAPI.getCountries().then(value => {
      debugger;
      CountryActions.countriesFetched(value);
    });

    return {};
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.COUNTRIES_FETCHED:
        for (const country of action.countries) {
          _countries[country.id] = country;
        }
        break;
      default:
        return;
    }

    this.__emitChange();
  }
};

module.exports = new CountryStore(Dispatcher);
