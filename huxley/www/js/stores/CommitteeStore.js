/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var CommitteeActions = require('actions/CommitteeActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');


var _committees = [];

class CommitteeStore extends Store {
  getCommittees() {
    if (_committees.length) {
      return _committees;
    }

    ServerAPI.getCommittees().then(value => {
      CommitteeActions.committeesFetched(value);
    });
    
    return [];
  }

  getSpecialCommittees() {
    return this.getCommittees().filter(committee => committee.special);
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.COMMITTEES_FETCHED:
        _committees = action.committees;
        break;
      default:
        return;
    }

    this.__emitChange();
  }
};

module.exports = new CommitteeStore(Dispatcher);
