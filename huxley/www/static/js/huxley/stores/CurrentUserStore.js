/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('../constants/ActionConstants');
var Dispatcher = require('../dispatcher/Dispatcher');
var EventEmitter = require('events').EventEmitter;

var invariant = require('react/lib/invariant');

var CHANGE_EVENT = 'change';

var _currentUser = null;
var _bootstrapped = false;

var CurrentUserStore = {...EventEmitter.prototype,
  getCurrentUser() {
    _assertBootstrapped();
    return _currentUser;
  },

  emitChange() {
    _assertBootstrapped();
    this.emit(CHANGE_EVENT);
  },

  addChangeListener(callback) {
    _assertBootstrapped();
    this.on(CHANGE_EVENT, callback);
  },

  removeChangeListener(callback) {
    _assertBootstrapped();
    this.removeListener(CHANGE_EVENT, callback);
  }
};

Dispatcher.register((action) => {
  switch (action.actionType) {
    case ActionConstants.BOOTSTRAP:
      _bootstrap();
      break;
    case ActionConstants.LOGIN:
      _currentUser = action.user;
      break;
    case ActionConstants.LOGOUT:
      _currentUser = {};
      break;
  }

  CurrentUserStore.emitChange();
});

function _bootstrap() {
  invariant(
    !_bootstrapped,
    'CurrentUserStore can only be bootstrapped once.'
  );
  invariant(
    global.currentUser !== undefined,
    'currentUser must be defined to bootstrap CurrentUserStore.'
  );

  _currentUser = global.currentUser;
  delete global.currentUser;
  _bootstrapped = true;
}

function _assertBootstrapped() {
  invariant(
    _bootstrapped,
    'CurrentUserStore must be bootstrapped before being used.'
  );
}

module.exports = CurrentUserStore;
