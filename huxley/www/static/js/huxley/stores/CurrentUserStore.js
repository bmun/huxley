/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('../constants/ActionConstants');
var Dispatcher = require('../dispatcher/Dispatcher');
var EventEmitter = require('events').EventEmitter;
var User = require('../User');

var invariant = require('react/lib/invariant');
var merge = require('react/lib/merge');

var CHANGE_EVENT = 'change';

var _currentUser = null;
var _bootstrapped = false;

function _assertBootstrapped() {
  invariant(
    _bootstrapped,
    'CurrentUserStore must be bootstrapped before being used.'
  );
}

var CurrentUserStore = merge(EventEmitter.prototype, {
  bootstrap: function() {
    invariant(
      !_bootstrapped,
      'CurrentUserStore can only be bootstrapped once.'
    );
    invariant(
      global.currentUser !== undefined,
      'currentUser must be defined to bootstrap CurrentUserStore.'
    );

    _currentUser = new User(global.currentUser);
    delete global.currentUser;
    _bootstrapped = true;
  },

  getCurrentUser: function() {
    _assertBootstrapped();
    return _currentUser;
  },

  emitChange: function() {
    _assertBootstrapped();
    this.emit(CHANGE_EVENT);
  },

  addChangeListener: function(callback) {
    _assertBootstrapped();
    this.on(CHANGE_EVENT, callback);
  },

  removeChangeListener: function(callback) {
    _assertBootstrapped();
    this.removeListener(CHANGE_EVENT, callback);
  }
});

Dispatcher.register(function(action) {
  switch (action.actionType) {
    case ActionConstants.LOGIN:
      _currentUser && _currentUser.destroy();
      _currentUser = new User(action.user);
      break;
    case ActionConstants.LOGOUT:
      _currentUser = new User();
      break;
  }

  CurrentUserStore.emitChange();
});

module.exports = CurrentUserStore;
