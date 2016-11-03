/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');


var _delegatePromises = {};
var _delegates = []

class DelegateStore extends Store {
  getDelegates(schoolID, callback) {
    if (!_delegatePromises[schoolID]) {
      _delegatePromises[schoolID] = ServerAPI.getDelegates(schoolID);
    }
    if (callback) {
      _delegatePromises[schoolID].then(function(value) {
        _delegates = value;
        callback(value);
      });
    }
    return _delegates;
  }

  deleteDelegate(delegate) {
    ServerAPI.deleteDelegate(delegate.id);
    var index = _delegates.indexOf(delegate);
    if (index != -1) {
      _delegates.splice(index,1);
    }
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.DELETE_DELEGATE:
        this.deleteDelegate(action.delegate);
        break;
      default:
        return;
    }

    this.__emitChange();
  }
};

module.exports = new DelegateStore(Dispatcher);
