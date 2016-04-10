/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Promise = require('es6-promise').Promise;
var Dispatcher = require('../dispatcher/Dispatcher');
var {Store} = require('flux/utils');


var _committeePromise = null;

class CommitteeStore extends Store {
  getCommittees(callback) {
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
  }

  getSpecialCommittees(callback) {
    this.getCommittees(function(committees) {
      callback(committees.filter(function(committee) {
        return committee.special;
      }));
    });
  }

  __onDispatch(action) {
    // This method must be overwritten
    return;
  }
};

module.exports = new CommitteeStore(Dispatcher);
