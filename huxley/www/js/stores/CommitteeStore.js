/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */
//@flow
"use strict";

import ActionConstants from "constants/ActionConstants";
import { CommitteeActions } from "actions/CommitteeActions";
import { Dispatcher } from "dispatcher/Dispatcher";
import { ServerAPI } from "lib/ServerAPI";
import { Store } from "flux/utils";

import type {Committee} from "utils/types";

var _committees: {[number]: Committee} = {};

class CommitteeStore extends Store {
  getCommittees(): {[number]: Committee} {
    if (Object.keys(_committees).length) {
      return _committees;
    }

    ServerAPI.getCommittees().then((value) => {
      CommitteeActions.committeesFetched(value);
    });

    return {};
  }

  getSpecialCommittees(): {[string]: Committee} {
    //$FlowFixMe
    var specialCommitteesArray = Object.values(this.getCommittees()).filter(
      (committee: Committee) => committee.special
    );
    var specialCommittees = {};
    for (const committee of specialCommitteesArray) {
      specialCommittees[committee.id] = committee;
    }
    return specialCommittees;
  }

  updateCommittee(committeeID: number, delta: any, onError: any) {
    const committee = { ..._committees[committeeID], ...delta };
    ServerAPI.updateCommittee(committeeID, committee).catch(onError);
    _committees[committeeID] = committee;
  }

  __onDispatch(action: any) {
    switch (action.actionType) {
      case ActionConstants.COMMITTEES_FETCHED:
        for (const committee of action.committees) {
          _committees[committee.id] = committee;
        }
        break;
      case ActionConstants.UPDATE_COMMITTEE:
        this.updateCommittee(
          action.committeeID,
          action.delta,
          action.onError
        );
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

const committeeStore: CommitteeStore = new CommitteeStore(Dispatcher);
export { committeeStore as CommitteeStore };
