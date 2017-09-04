/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var CurrentUserStore = require('stores/CurrentUserStore');
var Dispatcher = require('dispatcher/Dispatcher');
var RegistrationActions = require('actions/RegistrationActions');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');

var _registration = null;
var _previousUserID = -1;

class RegistrationStore extends Store {
  getRegistration(schoolID, conferenceID) {
    if (
      _registration &&
      _registration.school == schoolID &&
      _registration.conference == conferenceID
    ) {
      return _registration;
    }

    ServerAPI.getRegistration(schoolID, conferenceID).then(value => {
      RegistrationActions.registrationFetched(value[0]);
    });

    return null;
  }

  updateRegistration(registrationID, delta, onError) {
    const registration = {..._registration, ...delta};
    ServerAPI.updateRegistration(registrationID, registration).catch(onError);
    _registration = registration;
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.REGISTRATION_FETCHED:
        _registration = action.registration;
        break;
      case ActionConstants.UPDATE_REGISTRATION:
        this.updateRegistration(
          action.registrationID,
          action.delta,
          action.onError,
        );
        break;
      case ActionConstants.LOGIN:
        var userID = CurrentUserStore.getCurrentUser().id;
        if (userID != _previousUserID) {
          _registration = null;
          _previousUserID = userID;
        }
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

module.exports = new RegistrationStore(Dispatcher);
