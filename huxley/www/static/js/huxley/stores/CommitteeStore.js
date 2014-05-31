/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');

var _committeeRequest = null;

var CommitteeStore = {
  getCommittees: function(callback) {
    if (!_committeeRequest) {
      _committeeRequest = $.ajax({
        type: 'GET',
        url: '/api/committees',
        dataType: 'json'
      });
    }
    _committeeRequest.done(function(data, textStatus, jqXHR) {
      callback(jqXHR.responseJSON);
    });
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
