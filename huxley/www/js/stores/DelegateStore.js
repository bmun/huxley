/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var DelegateActions = require('actions/DelegateActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');


var _schoolsDelegates = {};
var _delegates = {};

class DelegateStore extends Store {
  getDelegates(schoolID) {
    if (_schoolsDelegates[schoolID]) {
      return _schoolsDelegates[schoolID];
    }

    ServerAPI.getDelegates(schoolID).then(value => {
      _schoolsDelegates[schoolID] = value;
      for (var i = 0; i < value.length; i++) {
        var delegate = value[i];
        _delegates[delegate.id] = delegate;
      }
      DelegateActions.delegatesFetched();
    });

    return [];
  }

  deleteDelegate(delegateID) {
    ServerAPI.deleteDelegate(delegateID);
    var schoolID = _delegates[delegateID].school;
    delete _delegates[delegateID];
    _schoolsDelegates[schoolID] = _schoolsDelegates[schoolID].filter(d => d.id !== delegateID);
  }

  addDelegate(delegate) {
    _delegates[delegate.id] = delegate;
    _schoolsDelegates[delegate.school].push(delegate);
  }

  updateDelegate(delegateID, delta) {
    ServerAPI.updateDelegate(delegateID, {
      name: delta.name,
      email: delta.email,
    });
    var delegate = _delegates[delegateID];
    delegate.name = delta.name;
    delegate.email = delta.email;
    _delegates[delegateID] = delegate;
    _schoolsDelegates[delegate.school] = _schoolsDelegates[delegate.school].map(d => d.id == delegate.id ? delegate : d);
  }

  updateDelegates(schoolID, delegates) {
    ServerAPI.updateSchoolDelegates(
      schoolID,
      JSON.stringify(delegates)
    )
    for (var i = 0; i < delegates.length; i++) {
      var delegate = delegates[i];
      _delegates[delegate.id] = delegate;
    }
    _schoolsDelegates[schoolID] = delegates;
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.DELETE_DELEGATE:
        this.deleteDelegate(action.delegateID);
        break;
      case ActionConstants.ADD_DELEGATE:
        this.addDelegate(action.delegate);
        break;
      case ActionConstants.UPDATE_DELEGATE:
        this.updateDelegate(action.delegateID, action.delta);
        break;
      case ActionConstants.DELEGATES_FETCHED:
        break;
      case ActionConstants.UPDATE_DELEGATES:
        this.updateDelegates(action.schoolID, action.delegates);
      default:
        return;
    }

    this.__emitChange();
  }
};

module.exports = new DelegateStore(Dispatcher);
