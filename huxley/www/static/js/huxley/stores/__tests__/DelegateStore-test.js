/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/DelegateStore');

describe('DelegateStore', () => {
  var DelegateStore;
  var Dispatcher;
  var ServerAPI;

  var mockDelegates, mockSchoolId;

  beforeEach(() => {
    DelegateStore = require('stores/DelegateStore');
    Dispatcher = require('dispatcher/Dispatcher');
    ServerAPI = require('lib/ServerAPI');

    mockDelegates = [{id: 1, name: 'Jake'}, {id: 2, name: 'Nate'}];
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
        expect(ServerAPI.getDelegates).toBeCalledWith(mockSchoolId);
        expect(delegates).toEqual(mockDelegates);
      }),
    ]);
  });
});
