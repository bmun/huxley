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
      DelegateActions.delegatesFetched(schoolID, value);
    });

    return [];
  }

  deleteDelegate(delegateID, onError) {
    ServerAPI.deleteDelegate(delegateID).catch(onError);
    var schoolID = _delegates[delegateID].school;
    delete _delegates[delegateID];
    _schoolsDelegates[schoolID] = _schoolsDelegates[schoolID].filter(d => d.id !== delegateID);
  }

  addDelegate(delegate) {
    _delegates[delegate.id] = delegate;
    _schoolsDelegates[delegate.school] = [..._schoolsDelegates[delegate.school], delegate];
  }

  updateDelegate(delegateID, delta, onError) {
    const delegate = {..._delegates[delegateID], ...delta};
    ServerAPI.updateDelegate(delegateID, delegate).catch(onError);
    _delegates[delegateID] = delegate;
    _schoolsDelegates[delegate.school] =
      _schoolsDelegates[delegate.school].map(d => d.id == delegate.id ? delegate : d);
  }

  updateDelegates(schoolID, delegates, onError) {
    ServerAPI.updateSchoolDelegates(schoolID, delegates).catch(onError);
    for (const delegate of delegates) {
      _delegates[delegate.id] = delegate;
    }
    _schoolsDelegates[schoolID] = delegates;
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.DELETE_DELEGATE:
        this.deleteDelegate(action.delegateID, action.onError);
        break;
      case ActionConstants.ADD_DELEGATE:
        this.addDelegate(action.delegate);
        break;
      case ActionConstants.UPDATE_DELEGATE:
        this.updateDelegate(action.delegateID, action.delta, action.onError);
        break;
      case ActionConstants.DELEGATES_FETCHED:
        _schoolsDelegates[action.schoolID] = action.delegates;
        for (const delegate of action.delegates) {
          _delegates[delegate.id] = delegate;
        }
        break;
      case ActionConstants.UPDATE_DELEGATES:
        this.updateDelegates(action.schoolID, action.delegates, action.onError);
        break;
      default:
        return;
    }

    this.__emitChange();
  }
};

module.exports = new DelegateStore(Dispatcher);
