/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../CommitteeStore');

describe('CommitteeStore', function() {
  var $;
  var CommitteeStore;

  var disc;
  var icj;
  var mockCommittees;

  beforeEach(function() {
    $ = require('jquery');
    CommitteeStore = require('../CommitteeStore');

    disc = {id: 1, name: 'DISC', special: false};
    icj = {id: 2, name: 'ICJ', special: true};
    mockCommittees = [disc, icj];

    $.ajax.mockImplementation(function(options) {
      options.success(null, null, {responseJSON: mockCommittees});
    });
  });

  it('requests the committees on first call and caches locally', function() {
    var calls = 0;

    CommitteeStore.getCommittees(function(committees) {
      calls++;
      expect($.ajax).toBeCalledWith({
        type: 'GET',
        url: '/api/committees',
        dataType: 'json',
        success: jasmine.any(Function),
      });
      expect(committees).toEqual(mockCommittees);
    });
    jest.runAllTimers();

    CommitteeStore.getCommittees(function(committees) {
      calls++;
      expect($.ajax.mock.calls.length).toBe(1);
      expect(committees).toEqual(mockCommittees);
    });
    jest.runAllTimers();

    expect(calls).toBe(2);
  });

  it('filters special committees', function() {
    var calls = 0;

    CommitteeStore.getSpecialCommittees(function(committees) {
      calls++;
      expect(committees).toEqual([icj]);
    });
    jest.runAllTimers();

    expect(calls).toBe(1);
  });
});
