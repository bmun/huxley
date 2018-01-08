/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var CommitteeFeedbackActions = require('actions/CommitteeFeedbackActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');

var _committeeFeedbacks = {};
var _committeeFeedbacksFetched = false;
var _feedbackSubmimtted = false;

class CommitteeFeedbackStore extends Store {
  getCommitteeFeedback(committeeID) {
    var feedbackIDs = Object.keys(_committeeFeedbacks);
    if (!_committeeFeedbacksFetched) {
      ServerAPI.getCommitteeFeedback(committeeID).then(value => {
        CommitteeFeedbackActions.committeeFeedbackFetched(value);
      });
      return [];
    }

    return feedbackIDs.map(id => _committeeFeedbacks[id]);
  }

  feedbackSubmitted() {
    return _feedbackSubmimtted;
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.ADD_COMMITTEE_FEEDBACK:
        _committeeFeedbacks[action.feedback.id] = action.feedback;
        _feedbackSubmimtted = true;
        break;
      case ActionConstants.COMMITTEE_FEEDBACK_FETCHED:
        for (const feedback of action.feedback) {
          _committeeFeedbacks[feedback.id] = feedback;
        }
        _committeeFeedbacksFetched = true;
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

module.exports = new CommitteeFeedbackStore(Dispatcher);
