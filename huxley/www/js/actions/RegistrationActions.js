/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var RegistrationActions = {
  registrationFetched(registration) {
    Dispatcher.dispatch({
      actionType: ActionConstants.REGISTRATION_FETCHED,
      registration: registration,
    });
  },

	updateRegistration() {
		Dispatcher.dispatch({});
	},
}

module.exports = RegistrationActions;
