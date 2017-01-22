/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var AssignmentActions = require('actions/AssignmentActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');


var _schoolsAssignments = {};
var _assignments = {};

class AssignmentStore extends Store {
  getAssignments(schoolID) {
    if (_schoolsAssignments[schoolID]) {
      return _schoolsAssignments[schoolID];
    }

    ServerAPI.getAssignments(schoolID).then(value => {
      AssignmentActions.assignmentsFetched(schoolID, value);
    });

    return [];
  }

  updateAssignment(assignmentID, delta, onError) {
    const assignment = {..._assignments[assignmentID], ...delta};
    ServerAPI.updateAssignment(assignmentID, assignment).catch(onError);
    _assignments[assignmentID] = assignment;
    _schoolsAssignments[assignment.school] =
      _schoolsAssignments[assignment.school].map(a => a.id == assignment.id ? assignment : a);
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.ASSIGNMENTS_FETCHED:
        _schoolsAssignments[action.schoolID] = action.assignments;
        for (const assignment of action.assignments) {
          _assignments[assignment.id] = assignment;
        }
        break;
      case ActionConstants.UPDATE_ASSIGNMENT:
        this.updateAssignment(action.assignmentID, action.delta, action.onError);
        break;
      default:
        return;
    }

    this.__emitChange();
  }
};

module.exports = new AssignmentStore(Dispatcher);
