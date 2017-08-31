/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');
var RegistrationActions = require('actions/RegistrationActions');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');

var _registration = null;

class RegistrationStore extends Store {
	getRegistration(schoolID, conferenceID) {
    if (_registration && _registration.school == schoolID && _registration.conference == conferenceID) {
		  return _registration;
    }

    ServerAPI.getRegistration(schoolID, conferenceID).then(value => {
      RegistrationActions.registrationFetched(value[0]);
    });

    return null;
	}

	updateRegistration(registrationID, delta, onError) {

	}

	__onDispatch(action) {
		switch (action.actionType) {
      case ActionConstants.REGISTRATION_FETCHED:
        _registration = action.registration;
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

module.exports = new RegistrationStore(Dispatcher);
