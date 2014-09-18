/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../AssignmentStore');

describe('AssignmentStore', function() {
  var $;
  var AssignmentStore;

  var mockAssignments;

  beforeEach(function() {
    $ = require('jquery');
    AssignmentStore = require('../AssignmentStore');

    mockAssignments = [{id: 1, school: 1}, {id: 2, school: 1}];

    $.ajax.mockImplementation(function(options) {
      options.success(null, null, {responseJSON: mockAssignments});
    });
  });

  it('requests the assignments on first call and caches locally', function() {
    var calls = 0;

    AssignmentStore.getAssignments(1, function(assignments) {
      calls++;
      expect($.ajax).toBeCalledWith({
        type: 'GET',
        url: '/api/schools/1/assignments',
        dataType: 'json',
        success: jasmine.any(Function),
    });
      expect(assignments).toEqual(mockAssignments);
    });
    jest.runAllTimers();

    AssignmentStore.getAssignments(1, function(assignments) {
      calls++;
      expect($.ajax.mock.calls.length).toBe(1);
      expect(assignments).toBe(mockAssignments);
    });
    jest.runAllTimers();

    expect(calls).toBe(2);
  });
});
