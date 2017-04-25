/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateActions = require('actions/DelegateActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');


var _delegates = {};
var _delegatesFetched = false;
var _previousUserID = -1;

class DelegateStore extends Store {
  getSchoolDelegates(schoolID) {
    var delegateIDs = Object.keys(_delegates);
    if (!_delegatesFetched) {
      ServerAPI.getDelegates(schoolID).then(value => {
        DelegateActions.delegatesFetched(value);
      });

      return [];
    }

    return delegateIDs.map(id => _delegates[id]);
  }

  getCommitteeDelegates(committeeID) {
    var delegateIDs = Object.keys(_delegates);
    if (!_delegatesFetched) {
      ServerAPI.getCommitteeDelegates(committeeID).then(value => {
        DelegateActions.delegatesFetched(value);
      });

      return [];
    }

    return delegateIDs.map(id => _delegates[id]);
  }

  deleteDelegate(delegateID, onError) {
    ServerAPI.deleteDelegate(delegateID).catch(onError);
    delete _delegates[delegateID];
  }

  addDelegate(delegate) {
    _delegates[delegate.id] = delegate;
  }

  updateDelegate(delegateID, delta, onError) {
    const delegate = {..._delegates[delegateID], ...delta};
    ServerAPI.updateDelegate(delegateID, delegate).catch(onError);
    _delegates[delegateID] = delegate;
  }

  updateDelegates(schoolID, delegates, onSuccess, onError) {
    ServerAPI.updateSchoolDelegates(schoolID, delegates).then(onSuccess).catch(onError);
    for (const delegate of delegates) {
      _delegates[delegate.id] = delegate;
    }
  }

  updateCommitteeDelegates(committeeID, delegates, onSuccess, onError) {
    ServerAPI.updateCommitteeDelegates(committeeID, delegates).then(onSuccess).catch(onError);
    for (const delegate of delegates) {
      _delegates[delegate.id] = delegate;
    }
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
        for (const delegate of action.delegates) {
          _delegates[delegate.id] = delegate;
        }
        _delegatesFetched = true;
        break;
      case ActionConstants.UPDATE_DELEGATES:
        this.updateDelegates(action.schoolID, action.delegates, action.onSuccess, action.onError);
        break;
      case ActionConstants.UPDATE_COMMITTEE_DELEGATES:
        this.updateCommitteeDelegates(action.committeeID, action.delegates, action.onSuccess, action.onError);
        break;
      case ActionConstants.LOGIN:
        var userID = CurrentUserStore.getCurrentUser().id;
        if (userID != _previousUserID) {
          _delegates = {};
          _delegatesFetched = false;
          _previousUserID = userID;
        }
        break;
      default:
        return;
    }

    this.__emitChange();
  }
};

module.exports = new DelegateStore(Dispatcher);
