/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var DelegateActions = {
  deleteDelegate(delegateID, onError) {
    Dispatcher.dispatch({
      actionType: ActionConstants.DELETE_DELEGATE,
      delegateID: delegateID,
      onError: onError,
    });
  },

  addDelegate(delegate) {
    Dispatcher.dispatch({
      actionType: ActionConstants.ADD_DELEGATE,
      delegate: delegate
    });
  },

  updateDelegate(delegateID, delta, onError) {
    Dispatcher.dispatch({
      actionType: ActionConstants.UPDATE_DELEGATE,
      delegateID: delegateID,
      delta: delta,
      onError: onError,
    });
  },

  delegatesFetched(schoolID, delegates) {
    Dispatcher.dispatch({
      actionType: ActionConstants.DELEGATES_FETCHED,
      schoolID: schoolID,
      delegates: delegates,
    });
  },

  updateDelegates(schoolID, delegates) {
    Dispatcher.dispatch({
      actionType: ActionConstants.UPDATE_DELEGATES,
      schoolID: schoolID,
      delegates: delegates
    });
  },

  updateCommitteeDelegates(committeeID, delegates) {
    Dispatcher.dispatch({
      actionType: ActionConstants.UPDATE_COMMITTEE_DELEGATES,
      committeeID: committeeID,
      delegates: delegates
    })
  }

};

module.exports = DelegateActions;
