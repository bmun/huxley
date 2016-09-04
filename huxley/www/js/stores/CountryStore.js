/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');


var _countryPromise = null;

class CountryStore extends Store {
  getCountries(callback) {
    if (!_countryPromise) {
      _countryPromise = ServerAPI.getCountries();
    }
    if (callback) {
      _countryPromise.then(callback);
    }
    return _countryPromise;
  }

  __onDispatch(action) {
    // This method must be overwritten
    return;
  }
};

module.exports = new CountryStore(Dispatcher);
