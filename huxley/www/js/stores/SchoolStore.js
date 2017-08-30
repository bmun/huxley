/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var CurrentUserStore = require('stores/CurrentUserStore');
var SchoolActions = require('actions/SchoolActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');

var _schools = {};
var _schoolsFetched = false;
var _previousUserID = -1;

class SchoolStore extends Store {
  getSchool(schoolID) {
    if (!_schoolsFetched) {
      return null;
    }

    return _schools[schoolID];
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.SCHOOLS_FETCHED:
        for (const school of action.schools) {
          _schools[school.id] = school;
        }
        _schoolsFetched = true;
        break;
      case ActionConstants.LOGIN:
        var userID = CurrentUserStore.getCurrentUser().id;
        if (userID != _previousUserID) {
          _schools = {};
          _schoolsFetched = false;
          _previousUserID = userID;
        }
        break;
      case ActionConstants.DELEGATE_FETCHED:
        const school = action.values.school;
        _schools[school.id] = school;
        _schoolsFetched = true;
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

module.exports = new SchoolStore(Dispatcher);
