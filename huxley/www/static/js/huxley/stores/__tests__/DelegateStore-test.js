/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../DelegateStore');

describe('DelegateStore', () => {
  var $;
  var DelegateStore;
  var Dispatcher;

  var mockDelegates, mockSchoolId;

  beforeEach(() => {
    $ = require('jquery');
    DelegateStore = require('../DelegateStore');
    Dispatcher = require('../../dispatcher/Dispatcher');

    mockDelegates = [{id: 1, name: 'Jake'}, {id: 2, name: 'Nate'}];
    mockSchoolId = 0;
    $.ajax.mockImplementation((options) => {
      options.success(null, null, {responseJSON: mockDelegates});
    });
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the delegates on first call and caches locally', () => {
    return Promise.all([
      DelegateStore.getDelegates(mockSchoolId, (delegates) => {
        expect($.ajax).toBeCalledWith({
          type: 'GET',
          url: '/api/schools/' + mockSchoolId + '/delegates',
          dataType: 'json',
          success: jasmine.any(Function),
        });
        expect(delegates).toEqual(mockDelegates);
      }),
      DelegateStore.getDelegates(mockSchoolId, (delegates) => {
        expect($.ajax.mock.calls.length).toBe(1);
        expect(delegates).toEqual(mockDelegates);
      }),
    ]);
  });
});
