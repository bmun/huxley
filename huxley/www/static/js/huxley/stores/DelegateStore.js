/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Promise = require('es6-promise').Promise;
var Dispatcher = require('../dispatcher/Dispatcher');
var {Store} = require('flux/utils');


var _delegatePromises = {};

class DelegateStore extends Store {
  getDelegates(schoolID, callback) {
    if (!_delegatePromises[schoolID]) {
      _delegatePromises[schoolID] = new Promise(function(resolve, reject) {
        $.ajax({
          type: 'GET',
          url: '/api/schools/'+schoolID+'/delegates',
          dataType: 'json',
          success: function(data, textStatus, jqXHR) {
            resolve(jqXHR.responseJSON);
          },
        });
      });
    }

    _delegatePromises[schoolID].then(callback);
  }

  __onDispatch(action) {
    // This method must be overwritten
    return;
  }
};

module.exports = new DelegateStore(Dispatcher);
