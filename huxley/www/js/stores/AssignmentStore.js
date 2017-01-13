/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var AssignmentActions = require('actions/AssignmentActions');
var CurrentUserStore = require('stores/CurrentUserStore');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');


var _assignments = {};
var _previousUserID = -1;


class AssignmentStore extends Store {
  getSchoolAssignments(schoolID) {
    var assignmentIDs = Object.keys(_assignments);
    if (!assignmentIDs.length) {
      ServerAPI.getAssignments(schoolID).then(value => {
        AssignmentActions.assignmentsFetched(value);
      });

      return [];
    }

    return assignmentIDs.map(id => _assignments[id]);
  }

  getCommitteeAssignments(committeeID) {
    var assignmentIDs = Object.keys(_assignments);
    if (!assignmentIDs.length) {
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

  getCommitteeAssignments(committeeID) {
    if (_committeeAssignments[committeeID]) {
      return _committeeAssignments[committeeID]; 
    }
    ServerAPI.getCommitteeAssignments(committeeID).then(value => {
      AssignmentActions.committeeAssignmentsFetched(committeeID, value);
    });

    return [];

  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.ASSIGNMENTS_FETCHED:
        for (const assignment of action.assignments) {
          _assignments[assignment.id] = assignment;
        }
        break;
      case ActionConstants.UPDATE_ASSIGNMENT:
        this.updateAssignment(action.assignmentID, action.delta, action.onError);
        break;
      case ActionConstants.LOGIN:
        var userID = CurrentUserStore.getCurrentUser().id;
        if(userID != _previousUserID) {
          _assignments = {};
          _previousUserID = userID;
        }
        break;
      case ActionConstants.LOGOUT:
        _assignments = {};
        break;
      default:
        return;
    }

    this.__emitChange();
  }
};

module.exports = new AssignmentStore(Dispatcher);
