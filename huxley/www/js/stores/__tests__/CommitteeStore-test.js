/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/CommitteeStore');

describe('CommitteeStore', () => {
  var CommitteeStore;
  var Dispatcher;
  var ServerAPI;

  var disc;
  var icj;
  var mockCommittees;

  beforeEach(() => {
    CommitteeStore = require('stores/CommitteeStore');
    Dispatcher = require('dispatcher/Dispatcher');
    ServerAPI = require('lib/ServerAPI');

    disc = {id: 1, name: 'DISC', special: false};
    icj = {id: 2, name: 'ICJ', special: true};
    mockCommittees = [disc, icj];

    ServerAPI.getCommittees.mockReturnValue(Promise.resolve(mockCommittees));
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the committees on first call and caches locally', () => {
    return Promise.all([
      CommitteeStore.getCommittees().then((committees) => {
        expect(committees).toEqual(mockCommittees);
      }),
      CommitteeStore.getCommittees().then((committees) => {
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
