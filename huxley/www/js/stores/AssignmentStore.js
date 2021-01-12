/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import ActionConstants from 'constants/ActionConstants';
import {AssignmentActions} from 'actions/AssignmentActions';
import {CurrentUserStore} from 'stores/CurrentUserStore';
import {Dispatcher} from 'dispatcher/Dispatcher';
import {ServerAPI} from 'lib/ServerAPI';
import {Store} from'flux/utils';

var _assignments = {};
var _assignmentsFetched = false;
var _previousUserID = -1;

class AssignmentStore extends Store {
  getSchoolAssignments(schoolID) {
    var assignmentIDs = Object.keys(_assignments);
    if (!_assignmentsFetched) {
      ServerAPI.getAssignments(schoolID).then(value => {
        AssignmentActions.assignmentsFetched(value);
      });

      return [];
    }

    return assignmentIDs.map(id => _assignments[id]);
  }

  getCommitteeAssignments(committeeID) {
    var assignmentIDs = Object.keys(_assignments);
    if (!_assignmentsFetched) {
      ServerAPI.getCommitteeAssignments(committeeID).then(value => {
        AssignmentActions.assignmentsFetched(value);
      });

      return [];
    }

    return assignmentIDs.map(id => _assignments[id]);
  }

  updateAssignment(assignmentID, delta, onError) {
    const assignment = {..._assignments[assignmentID], ...delta};
    ServerAPI.updateAssignment(assignmentID, assignment).catch(onError);
    _assignments[assignmentID] = assignment;
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.ASSIGNMENTS_FETCHED:
        for (const assignment of action.assignments) {
          _assignments[assignment.id] = assignment;
        }
        _assignmentsFetched = true;
        break;
      case ActionConstants.UPDATE_ASSIGNMENT:
        this.updateAssignment(
          action.assignmentID,
          action.delta,
          action.onError,
        );
        break;
      case ActionConstants.LOGIN:
        var userID = CurrentUserStore.getCurrentUser().id;
        if (userID != _previousUserID) {
          _assignments = {};
          _assignmentsFetched = false;
          _previousUserID = userID;
        }
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

const assignmentStore = new AssignmentStore(Dispatcher);
export {assignmentStore as AssignmentStore};
