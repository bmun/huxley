/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Dispatcher = require('../dispatcher/Dispatcher');
var {Store} = require('flux/utils');


var _countryPromise = null;

class CountryStore extends Store {
  getCountries(callback) {
    if (!_countryPromise) {
      _countryPromise = new Promise(function(resolve, reject) {
        $.ajax({
          type: 'GET',
          url: '/api/countries',
          dataType: 'json',
          success: function(data, textStatus, jqXHR) {
            resolve(jqXHR.responseJSON);
          },
        });
      });
    }

    _countryPromise.then(callback);
  }

  __onDispatch(action) {
    // This method must be overwritten
    return;
  }
};

module.exports = new CountryStore(Dispatcher);
