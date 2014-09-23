/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Promise = require('es6-promise').Promise;


var _committeePromise = null;

var CommitteeStore = {
  getCommittees: function(callback) {
    if (!_committeePromise) {
      _committeePromise = new Promise(function(resolve, reject) {
        $.ajax({
          type: 'GET',
          url: '/api/committees',
          dataType: 'json',
          success: function(data, textStatus, jqXHR) {
            resolve(jqXHR.responseJSON);
          },
        });
      });
    }

    _committeePromise.then(callback);
  },

  getSpecialCommittees: function(callback) {
    this.getCommittees(function(committees) {
      callback(committees.filter(function(committee) {
        return committee.special;
      }));
    });
  }
};

module.exports = CommitteeStore;
