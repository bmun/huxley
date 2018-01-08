/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/CommitteeFeedbackStore');

describe('CommitteeFeedbackStore', () => {
  var ActionConstants;
  var CommitteeFeedbackStore;
  var Dispatcher;
  var ServerAPI;

  var mockFeedbacks;
  var mockCommitteeID;
  var noFeedbackCommitteeID;
  var registerCallback;

  beforeEach(() => {
  	ActionConstants = require('constants/ActionConstants');
  	CommitteeFeedbackStore = require('stores/CommitteeFeedbackStore');
  	Dispatcher = require('dispatcher/Dispatcher');
  	ServerAPI = require('lib/ServerAPI');

  	registerCallback = function(action) {
      Dispatcher.isDispatching.mockReturnValue(true);
      Dispatcher.register.mock.calls[0][0](action);
      Dispatcher.isDispatching.mockReturnValue(false);
  	}

  	mockCommitteeID = 1;
  	noFeedbackCommitteeID = 0;

  	var mockFeedback1 = {
  		id: 1,
  		committee: mockCommitteeID,
  		comment: "Loved Committee"
  	};

  	var mockFeedback2 = {
  		id: 2,
  		committee: mockCommitteeID,
  		comment: "Joanne was a great chair"
  	};

  	mockFeedbacks = [mockFeedback1, mockFeedback2];

  	ServerAPI.getCommitteeFeedback.mockReturnValue(Promise.resolve(mockFeedbacks));
  	ServerAPI.createCommitteeFeedback.mockReturnValue(Promise.resolve({}));
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the feedback on the first call and caches locally', () => {
  	var feedback = CommitteeFeedbackStore.getCommitteeFeedback(mockCommitteeID);
  	expect(feedback.length).toEqual(0);
  	expect(ServerAPI.getCommitteeFeedback).toBeCalledWith(mockCommitteeID);

  	registerCallback({
  		actionType: ActionConstants.COMMITTEE_FEEDBACK_FETCHED,
  		feedback: mockFeedbacks,
  	});

  	feedback = CommitteeFeedbackStore.getCommitteeFeedback(mockCommitteeID);
  	expect(feedback).toEqual(mockFeedbacks);
  	expect(ServerAPI.getCommitteeFeedback.mock.calls.length).toEqual(1);

  });

  it('differentiates no feedback from not having fetched feedback', () => {
  	var feedback = CommitteeFeedbackStore.getCommitteeFeedback(noFeedbackCommitteeID);
  	expect(feedback.length).toEqual(0);
  	expect(ServerAPI.getCommitteeFeedback).toBeCalledWith(noFeedbackCommitteeID);

  	registerCallback({
  		actionType: ActionConstants.COMMITTEE_FEEDBACK_FETCHED,
  		feedback: [],
  	});

  	feedback = CommitteeFeedbackStore.getCommitteeFeedback(noFeedbackCommitteeID);
  	expect(feedback).toEqual([]);
  	expect(ServerAPI.getCommitteeFeedback.mock.calls.length).toEqual(1);

  });

  it('emits a change when the feedback is loaded', () => {
  	var callback = jest.genMockFunction();
  	CommitteeFeedbackStore.addListener(callback);
  	expect(callback).not.toBeCalled();
  	registerCallback({
  		actionType: ActionConstants.COMMITTEE_FEEDBACK_FETCHED,
  		feedback: mockFeedbacks,
  	});
  	expect(callback).toBeCalled();
  });

  it('adds a feedback and emits a change and caches that feedback was submitted', () => {
  	registerCallback({
  		actionType: ActionConstants.COMMITTEE_FEEDBACK_FETCHED,
  		feedback: mockFeedbacks,
  	});

	var callback = jest.genMockFunction();
  	CommitteeFeedbackStore.addListener(callback);
  	expect(callback).not.toBeCalled();

  	var new_feedback = {
  		id: 3,
  		committee: mockCommitteeID,
  		comment: "Lol I chewed gum in the back the whole time"
  	};

  	var feedback_submitted = CommitteeFeedbackStore.feedbackSubmitted();
  	expect(feedback_submitted).toBe(false);

  	registerCallback({
  		actionType: ActionConstants.ADD_COMMITTEE_FEEDBACK,
  		feedback: new_feedback,
  	});
  	expect(callback).toBeCalled();

  	var feedback = CommitteeFeedbackStore.getCommitteeFeedback(mockCommitteeID);
  	expect(feedback.length).toEqual(3);
  	expect(new_feedback).toEqual(feedback[2]);

  	
	feedback_submitted = CommitteeFeedbackStore.feedbackSubmitted();
  	expect(feedback_submitted).toBe(true);
  });

});