/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import ActionConstants from 'constants/ActionConstants';
import {CommitteeActions} from 'actions/CommitteeActions';
import {Dispatcher} from 'dispatcher/Dispatcher';
import {ServerAPI} from 'lib/ServerAPI';
import {Store} from'flux/utils';

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
      default:
        return;
    }

    this.__emitChange();
  }
}

const committeeStore = new CommitteeStore(Dispatcher);
export {committeeStore as CommitteeStore};
