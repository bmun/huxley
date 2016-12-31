/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var AssignmentActions = {
  assignmentsFetched(schoolID, assignments) {
    Dispatcher.dispatch({
      actionType: ActionConstants.ASSIGNMENTS_FETCHED,
      schoolID: schoolID,
      assignments: assignments,
    });
  },

  updateAssignment(assignmentID, delta) {
    Dispatcher.dispatch({
      actionType: ActionConstants.UPDATE_ASSIGNMENT,
      assignmentID: assignmentID,
      delta: delta,
    });
  }
};

module.exports = AssignmentActions;
