/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
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

    $.ajax.mockReturnValue({
      done: function(callback) {
        callback(null, null, {responseJSON: mockCommittees});
      }
    });
  });

  it('requests the committees on first call and caches locally', function() {
    CommitteeStore.getCommittees(function(committees) {
      expect($.ajax).toBeCalledWith({
        type: 'GET',
        url: '/api/committees',
        dataType: 'json'
      });
      expect(committees).toEqual(mockCommittees);
    });
    CommitteeStore.getCommittees(function(committees) {
      expect($.ajax.mock.calls.length).toBe(1);
      expect(committees).toEqual(mockCommittees);
    });
  });

  it('filters special committees', function() {
    CommitteeStore.getSpecialCommittees(function(committees) {
      expect(committees).toEqual([icj]);
    });
  });
});
