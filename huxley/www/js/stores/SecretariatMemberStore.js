/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var SecretariatMemberActions = require('actions/SecretariatMemberActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');

var _secretariatMembers = {};
var _secretariatMembersFetched = false;

class SecretariatMemberStore extends Store {
  getSecretariatMembers(committeeID) {
    var secretariatMemberIDs = Object.keys(_secretariatMembers);
    if (!_secretariatMembersFetched) {
      ServerAPI.getSecretariatMembers(committeeID).then(value => {
        SecretariatMemberActions.secretariatMembersFetched(value);
      });
      return [];
    }
    return secretariatMemberIDs.map(id => _secretariatMembers[id]);
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.SECRETARIAT_MEMBERS_FETCHED:
        for (const member of action.secretariatMembers) {
          _secretariatMembers[member.id] = member;
        }
        _secretariatMembersFetched = true;
        break;
      default:
        break;
    }

    this.__emitChange();
  }
}

module.exports = new SecretariatMemberStore(Dispatcher);
