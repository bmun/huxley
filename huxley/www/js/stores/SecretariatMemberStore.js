/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import ActionConstants from 'constants/ActionConstants';
import {SecretariatMemberActions} from 'actions/SecretariatMemberActions';
import {Dispatcher} from 'dispatcher/Dispatcher';
import ServerAPI from 'lib/ServerAPI';
import {Store} from'flux/utils';

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

const secretariatMemberStore = new SecretariatMemberStore(Dispatcher);
export {secretariatMemberStore as SecretariatMemberStore};
