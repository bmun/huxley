/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/AssignmentStore');

describe('AssignmentStore', () => {
  var ActionConstants;
  var AssignmentStore;
  var Dispatcher;
  var ServerAPI;

  var mockAssignments, mockSchoolID;
  var registerCallback;

  beforeEach(() => {
    ActionConstants = require('constants/ActionConstants');
    AssignmentStore = require('stores/AssignmentStore');
    Dispatcher = require('dispatcher/Dispatcher');
    ServerAPI = require('lib/ServerAPI');

    registerCallback = function(action) {
      Dispatcher.isDispatching.mockReturnValue(true);
      Dispatcher.register.mock.calls[0][0](action);
      Dispatcher.isDispatching.mockReturnValue(false);
    };

    mockSchoolID = 1
    mockAssignments = [
      {id: 1, school: mockSchoolID, rejected: false},
      {id: 2, school: mockSchoolID, rejected: false}
    ];
    ServerAPI.getAssignments.mockReturnValue(Promise.resolve(mockAssignments));
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the assignments on first call and caches locally', () => {
    var assignments = AssignmentStore.getAssignments(mockSchoolID);
    expect(assignments.length).toEqual(0);
    expect(ServerAPI.getAssignments).toBeCalledWith(mockSchoolID);

    registerCallback({
      actionType: ActionConstants.ASSIGNMENTS_FETCHED,
      schoolID: mockSchoolID,
      assignments: mockAssignments
    });

    assignments = AssignmentStore.getAssignments(mockSchoolID);
    expect(assignments).toEqual(mockAssignments);
    expect(ServerAPI.getAssignments.mock.calls.length).toEqual(1);
  });

  it('emits a change when the assignments are loaded', function() {
    var callback = jest.genMockFunction();
    AssignmentStore.addListener(callback);
    expect(callback).not.toBeCalled();
    registerCallback({
      actionType: ActionConstants.ASSIGNMENTS_FETCHED,
      schoolID: mockSchoolID,
      assignments: mockAssignments
    });
    expect(callback).toBeCalled();
  });

  it('updates an assignment and emits a change', function() {
    registerCallback({
      actionType: ActionConstants.ASSIGNMENTS_FETCHED,
      schoolID: mockSchoolID,
      assignments: mockAssignments
    });

    var callback = jest.genMockFunction();
    AssignmentStore.addListener(callback);
    expect(callback).not.toBeCalled();

    registerCallback({
      actionType: ActionConstants.UPDATE_ASSIGNMENT,
      assignmentID: 1,
      delta: {rejected: true}
    });
    expect(callback).toBeCalled();

    expect(ServerAPI.updateAssignment).toBeCalled();
    var assignments = AssignmentStore.getAssignments(mockSchoolID);
    expect(assignments[0]['rejected']).toBe(true);
  });
});
