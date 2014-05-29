/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');

var EventEmitter = require('events').EventEmitter;
var merge = require('react/lib/merge');

var _countryRequest = null;

var CountryStore = merge(EventEmitter.prototype, {
  getCountries: function(callback) {
    if (!_countryRequest) {
      _countryRequest = $.ajax({
        type: 'GET',
        url: '/api/countries',
        dataType: 'json'
      });
    }
    _countryRequest.done(function(data, textStatus, jqXHR) {
      callback(jqXHR.responseJSON);
    });
  }
});

module.exports = CountryStore;
