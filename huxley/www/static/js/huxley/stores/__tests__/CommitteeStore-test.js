/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/CommitteeStore');

describe('CommitteeStore', () => {
  var $;
  var CommitteeStore;
  var Dispatcher;

  var disc;
  var icj;
  var mockCommittees;

  beforeEach(() => {
    $ = require('jquery');
    CommitteeStore = require('stores/CommitteeStore');
    Dispatcher = require('dispatcher/Dispatcher');

    disc = {id: 1, name: 'DISC', special: false};
    icj = {id: 2, name: 'ICJ', special: true};
    mockCommittees = [disc, icj];

    $.ajax.mockImplementation((options) => {
      options.success(null, null, {responseJSON: mockCommittees});
    });
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the committees on first call and caches locally', () => {
    return Promise.all([
      CommitteeStore.getCommittees().then((committees) => {
        expect($.ajax).toBeCalledWith({
          type: 'GET',
          url: '/api/committees',
          dataType: 'json',
          success: jasmine.any(Function),
        });
        expect(committees).toEqual(mockCommittees);
      }),
      CommitteeStore.getCommittees().then((committees) => {
        expect($.ajax.mock.calls.length).toBe(1);
        expect(committees).toEqual(mockCommittees);
      }),
    ]);
  });

  it('filters special committees', () => {
    return CommitteeStore.getSpecialCommittees().then((committees) => {
      expect(committees).toEqual([icj]);
    });
  });
});
