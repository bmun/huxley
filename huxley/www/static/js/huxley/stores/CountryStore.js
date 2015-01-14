/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Promise = require('es6-promise').Promise;


var _countryPromise = null;

var CountryStore = {
  getCountries: function(callback) {
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
  },
};

module.exports = CountryStore;
