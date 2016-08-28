/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
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

    if (callback) {
      _committeePromise.then(callback);
    }
    return _committeePromise;
  }

  getSpecialCommittees(callback) {
    var p = this.getCommittees().then((committees) => {
      return committees.filter((committee) => committee.special);
    });
    if (callback) {
      p.then(callback);
    }
    return p;
  }

  __onDispatch(action) {
    // This method must be overwritten
    return;
  }
};

module.exports = new CommitteeStore(Dispatcher);
