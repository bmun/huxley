/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../AssignmentStore');

describe('AssignmentStore', function() {
  var console = require('console');
  var $;
  var AssignmentStore;

  var mockAssignments;

  beforeEach(function() {
    $ = require('jquery');
    AssignmentStore = require('../AssignmentStore');

    mockAssignments = [{id: 1, school: 0}, {id: 2, school: 0}];

    $.ajax.mockReturnValue({
        done: function(callback) {
          callback(null, null, {responseJSON: mockAssignments});
        }
    });
  });

  it('requests the assignments on first call and caches locally', function() {
    AssignmentStore.getAssignments(1, function(assignments) {
      expect($.ajax).toBeCalledWith({
        type: 'GET',
        url: '/api/schools/1/assignments',
        dataType: 'json'
    });
      expect(assignments).toEqual(mockAssignments);
    });
    AssignmentStore.getAssignments(0, function(assignments) {
      expect($.ajax.mock.calls.length).toBe(1);
      expect(assignments).toBe(mockAssignments);
    });
  });
});
