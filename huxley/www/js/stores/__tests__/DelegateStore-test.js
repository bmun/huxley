/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/DelegateStore');

describe('DelegateStore', () => {
  var ActionConstants;
  var DelegateStore;
  var Dispatcher;
  var ServerAPI;

  var mockDelegates, mockSchoolId;

  beforeEach(() => {
    ActionConstants = require('constants/ActionConstants');
    DelegateStore = require('stores/DelegateStore');
    Dispatcher = require('dispatcher/Dispatcher');
    ServerAPI = require('lib/ServerAPI');

    mockDelegates = [{id: 1, name: 'Jake', email: ''}, {id: 2, name: 'Nate', email: ''}];
    mockSchoolId = 0;
    ServerAPI.getDelegates.mockReturnValue(Promise.resolve(mockDelegates));
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the delegates on first call and caches locally', () => {
    return Promise.all([
      DelegateStore.getDelegates(mockSchoolId, (delegates) => {
        expect(ServerAPI.getDelegates).toBeCalledWith(mockSchoolId);
        expect(delegates).toEqual(mockDelegates);
      }),
      DelegateStore.getDelegates(mockSchoolId, (delegates) => {
        expect(ServerAPI.getDelegates.mock.calls.length).toBe(1);
        expect(delegates).toEqual(mockDelegates);
      }),
    ]);
  });

  it('adds a delegate', () => {
    return Promise.resolve(
      DelegateStore.getDelegates(mockSchoolId, (delegates) => {
        expect(delegates).toEqual(mockDelegates);
        DelegateStore.addDelegate({id: 3, name: 'Trevor', email: ''});
        expect(DelegateStore.getDelegates(mockSchoolId).length).toEqual(3);
      })
    );
  });

  it('deletes a delegate', () => {
    return Promise.resolve(
      DelegateStore.getDelegates(mockSchoolId, (delegates) => {
        expect(delegates).toEqual(mockDelegates);
        DelegateStore.deleteDelegate(mockDelegates[0]);
        expect(DelegateStore.getDelegates(mockSchoolId).length).toEqual(1);
      })
    );
  });

  it('updates a delegate', () => {
    return Promise.all([
      DelegateStore.getDelegates(mockSchoolId, (delegates) => {
        expect(delegates).toEqual(mockDelegates);
        var delta = {name: "Jake Moskowitz", email: "jake@bmun.org"};
        DelegateStore.updateDelegate(1, delta);
      }),
      DelegateStore.getDelegates(mockSchoolId, (delegates) => {
        var updatedDelegate = delegates[0];
        expect(updatedDelegate.name).toBe("Jake Moskowitz");
        expect(updatedDelegate.email).toBe("jake@bmun.org");
      })
    ]);
  });

  it('updates delegates in bulk', () => {
    var updatedDelegates = [
      {id: 1, name: 'Jake Moskowitz', email: ''},
      {id: 2, name: 'Nathaniel Parke', email: ''}
    ];
    return Promise.all([
      DelegateStore.getDelegates(mockSchoolId, (delegates) => {
        expect(delegates).toEqual(mockDelegates);
        DelegateStore.updateDelegates(mockSchoolId, updateDelegates);
      }),
      DelegateStore.getDelegates(mockSchoolId, (delegates) => {
        expect(delegates).toEqual(updatedDelegates);
      })
    ]);
  });
});
