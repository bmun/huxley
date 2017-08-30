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

var _committees = {};

class CommitteeStore extends Store {
  getCommittees() {
    if (Object.keys(_committees).length) {
      return _committees;
    }

    ServerAPI.getCommittees().then(value => {
      CommitteeActions.committeesFetched(value);
    });

    return {};
  }

  getSpecialCommittees() {
    var specialCommitteesArray = Object.values(this.getCommittees()).filter(
      committee => committee.special,
    );
    var specialCommittees = {};
    for (const committee of specialCommitteesArray) {
      specialCommittees[committee.id] = committee;
    }
    return specialCommittees;
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.COMMITTEES_FETCHED:
        for (const committee of action.committees) {
          _committees[committee.id] = committee;
        }
        break;
      case ActionConstants.DELEGATE_FETCHED:
        const committee = action.values.committee;
        _committees[committee.id] = committee;
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

module.exports = new CommitteeStore(Dispatcher);
