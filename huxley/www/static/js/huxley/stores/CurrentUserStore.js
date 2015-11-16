/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('../constants/ActionConstants');
var Dispatcher = require('../dispatcher/Dispatcher');
var {Store} = require('flux/utils');

var invariant = require('fbjs/lib/invariant');

class CurrentUserStore extends Store {
  constructor(dispatcher) {
    super(dispatcher);
    this._currentUser = null;
    this._isBootstrapped = false;
  }

  getCurrentUser() {
    this._assertBootstrapped();
    return this._currentUser;
  }

  getFinalized() {
    this._assertBootstrapped();
    return this._currentUser.school.assignments_finalized;
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
      case ActionConstants.UPDATE_SCHOOL:
        this._currentUser.school = action.school;
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
    this._assignmentsFinalized = this._currentUser.school.assignmentsFinalized;
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
