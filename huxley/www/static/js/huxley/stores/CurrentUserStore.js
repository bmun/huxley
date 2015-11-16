/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('../constants/ActionConstants');
var Dispatcher = require('../dispatcher/Dispatcher');
var {Store} = require('flux/utils');

var invariant = require('react/lib/invariant');

class CurrentUserStore extends Store {
  constructor(dispatcher) {
    super(dispatcher);
    this._currentUser = null;
    this._isBootstrapped = false;
    this._assignmentsFinalized = false;
  }

  getCurrentUser() {
    this._assertBootstrapped();
    return this._currentUser;
  }

  getFinalized() {
    this._assertBootstrapped();
    return this._assignmentsFinalized;
  }

  addListener(callback) {
    this._assertBootstrapped();
    return super.addListener(callback);
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.BOOTSTRAP:
        this._bootstrap();
        break;
      case ActionConstants.LOGIN:
        this._currentUser = action.user;
        break;
      case ActionConstants.LOGOUT:
        this._currentUser = {};
        break;
      case ActionConstants.FINALIZE:
        this._assignmentsFinalized = action.finalize;
        break;
      default:
        return;
    }

    this.__emitChange();
  }

  _bootstrap() {
    invariant(
      !this._isBootstrapped,
      'CurrentUserStore can only be bootstrapped once.'
    );
    invariant(
      global.currentUser !== undefined,
      'currentUser must be defined to bootstrap CurrentUserStore.'
    );

    this._currentUser = global.currentUser;
    delete global.currentUser;
    this._isBootstrapped = true;
  }

  _assertBootstrapped() {
    invariant(
      this._isBootstrapped,
      'CurrentUserStore must be bootstrapped before being used.'
    );
  }
}

module.exports = new CurrentUserStore(Dispatcher);
