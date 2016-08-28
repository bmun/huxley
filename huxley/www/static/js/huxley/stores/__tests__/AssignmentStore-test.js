/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../AssignmentStore');

describe('AssignmentStore', () => {
  var $;
  var AssignmentStore;
  var Dispatcher;

  var mockAssignments;

  beforeEach(() => {
    $ = require('jquery');
    AssignmentStore = require('../AssignmentStore');
    Dispatcher = require('../../dispatcher/Dispatcher');

    mockAssignments = [{id: 1, school: 1}, {id: 2, school: 1}];

    $.ajax.mockImplementation((options) => {
      options.success(null, null, {responseJSON: mockAssignments});
    });
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the assignments on first call and caches locally', () => {
    return Promise.all([
      AssignmentStore.getAssignments(1).then((assignments) => {
        expect($.ajax).toBeCalledWith({
          type: 'GET',
          url: '/api/schools/1/assignments',
          dataType: 'json',
          success: jasmine.any(Function),
        });
        expect(assignments).toEqual(mockAssignments);
      }),
      AssignmentStore.getAssignments(1).then((assignments) => {
        expect($.ajax.mock.calls.length).toBe(1);
        expect(assignments).toBe(mockAssignments);
      }),
    ]);
  });
});
