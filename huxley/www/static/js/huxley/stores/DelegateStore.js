/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');


var _delegatePromises = {};

class DelegateStore extends Store {
  getDelegates(schoolID, callback) {
    if (!_delegatePromises[schoolID]) {
      _delegatePromises[schoolID] = ServerAPI.getDelegates(schoolID);
    }
    if (callback) {
      _delegatePromises[schoolID].then(callback);
    }
    return _delegatePromises[schoolID];
  }

  __onDispatch(action) {
    // This method must be overwritten
    return;
  }
};

module.exports = new DelegateStore(Dispatcher);
