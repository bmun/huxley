/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
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
      _schoolsAssignments[schoolID] = value;
      for (const assignment of value) {
        _assignments[assignment.id] = assignment;
      }
      AssignmentActions.assignmentsFetched();
    });

    return [];
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.ASSIGNMENTS_FETCHED:
        break;
      default:
        return;
    }

    this.__emitChange();
  }
};

module.exports = new AssignmentStore(Dispatcher);
