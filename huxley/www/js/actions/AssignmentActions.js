/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import ActionConstants from 'constants/ActionConstants';
import {Dispatcher} from 'dispatcher/Dispatcher';

var AssignmentActions = {
  assignmentsFetched(assignments) {
    Dispatcher.dispatch({
      actionType: ActionConstants.ASSIGNMENTS_FETCHED,
      assignments: assignments,
    });
  },

  updateAssignment(assignmentID, delta, onError) {
    Dispatcher.dispatch({
      actionType: ActionConstants.UPDATE_ASSIGNMENT,
      assignmentID: assignmentID,
      delta: delta,
      onError: onError,
    });
  },
};

export {AssignmentActions};
