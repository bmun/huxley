/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import ActionConstants from 'constants/ActionConstants';
import {Dispatcher} from 'dispatcher/Dispatcher';
import {ServerAPI} from 'lib/ServerAPI';
import {Store} from'flux/utils';

import invariant from 'invariant';

class CurrentUserStore extends Store {
  constructor(dispatcher) {
    super(dispatcher);
    this._currentUser = null;
    this._isBootstrapped = false;
  }

  getCurrentUser() {
    console.log(this.currentUser);
    this._assertBootstrapped();
    return this._currentUser;
  }

  addListener(callback) {
    this._assertBootstrapped();
    return super.addListener(callback);
  }

  updateSchool(schoolID, delta, onError) {
    ServerAPI.updateSchool(schoolID, delta).catch(onError);
    const user = this._currentUser;
    this._currentUser = {
      ...user,
      school: {...user.school, ...delta},
    };
  }

  updateUser(userID, delta, onSuccess, onError) {
    ServerAPI.updateUser(userID, delta).then(onSuccess, onError);

    const user = {
      ...this._currentUser,
      first_name: delta.first_name,
      last_name: delta.last_name,
    };
    this._currentUser = {
      ...user,
      school: {...user.school, ...delta.school},
    };
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
        this.updateSchool(action.schoolID, action.delta, action.onError);
        break;
      case ActionConstants.UPDATE_USER:
        this.updateUser(
          action.userID,
          action.delta,
          action.onSuccess,
          action.onError,
        );
        break;
      default:
        return;
    }

    this.__emitChange();
  }

  _bootstrap() {
    invariant(
      !this._isBootstrapped,
      'CurrentUserStore can only be bootstrapped once.',
    );
    invariant(
      global.currentUser !== undefined,
      'currentUser must be defined to bootstrap CurrentUserStore.',
    );

    this._currentUser = global.currentUser;
    global.currentUser = undefined;
    this._isBootstrapped = true;
  }

  _assertBootstrapped() {
    invariant(
      this._isBootstrapped,
      'CurrentUserStore must be bootstrapped before being used.',
    );
  }
}

const currentUserStore = new CurrentUserStore(Dispatcher);
export {currentUserStore as CurrentUserStore};
