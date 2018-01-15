/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var CommitteeFeedbackActions = {
  addCommitteeFeedback(feedback) {
    Dispatcher.dispatch({
      actionType: ActionConstants.ADD_COMMITTEE_FEEDBACK,
      feedback: feedback,
    });
  },

  committeeFeedbackFetched(feedback) {
    Dispatcher.dispatch({
      actionType: ActionConstants.COMMITTEE_FEEDBACK_FETCHED,
      feedback: feedback,
    });
  },
};

module.exports = CommitteeFeedbackActions;
