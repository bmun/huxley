/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/AssignmentStore');

describe('AssignmentStore', () => {
  var AssignmentStore;
  var Dispatcher;
  var ServerAPI;

  var mockAssignments;

  beforeEach(() => {
    AssignmentStore = require('stores/AssignmentStore');
    Dispatcher = require('dispatcher/Dispatcher');
    ServerAPI = require('lib/ServerAPI');

    mockAssignments = [{id: 1, school: 1}, {id: 2, school: 1}];
    ServerAPI.getAssignments.mockReturnValue(Promise.resolve(mockAssignments));
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the assignments on first call and caches locally', () => {
    return Promise.all([
      AssignmentStore.getAssignments(1).then((assignments) => {
        expect(ServerAPI.getAssignments).toBeCalledWith(1);
        expect(assignments).toEqual(mockAssignments);
      }),
      AssignmentStore.getAssignments(1).then((assignments) => {
        expect(ServerAPI.getAssignments).toBeCalledWith(1);
        expect(assignments).toBe(mockAssignments);
      }),
    ]);
  });
});
