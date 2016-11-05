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

  addDelegate(delegate) {
    _delegates.push(delegate);
  }

  updateDelegate(delegateID, name, email, schoolID) {
    ServerAPI.updateDelegate(delegateID, {
      name: name,
      email: email,
      school: schoolID
    });
    var _delegate = _delegates.find(function(delegate) {
      return delegate.id == delegateID;
    });
    _delegate.name = name;
    _delegate.email = email;
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.DELETE_DELEGATE:
        this.deleteDelegate(action.delegate);
        break;
      case ActionConstants.ADD_DELEGATE:
        this.addDelegate(action.delegate);
        break;
      case ActionConstants.UPDATE_DELEGATE:
        this.updateDelegate(
          action.delegateID,
          action.name,
          action.email,
          action.schoolID
        );
        break;
      default:
        return;
    }

    this.__emitChange();
  }
};

module.exports = new DelegateStore(Dispatcher);
