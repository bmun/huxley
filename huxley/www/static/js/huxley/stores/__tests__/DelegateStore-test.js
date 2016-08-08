/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../DelegateStore');

describe('DelegateStore', function() {
  var $;
  var DelegateStore;

  var mockDelegates, mockSchoolId;

  beforeEach(function() {
    $ = require('jquery');
    DelegateStore = require('../DelegateStore');
    Dispatcher = require('../../dispatcher/Dispatcher');

    mockDelegates = [{id: 1, name: 'Jake'}, {id: 2, name: 'Nate'}];
    mockSchoolId = 0;
    $.ajax.mockImplementation(function(options) {
      options.success(null, null, {responseJSON: mockDelegates});
    });
  });

  it('subscribes to the dispatcher', function() {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the delegates on first call and caches locally', function() {
    var calls = 0;

    DelegateStore.getDelegates(mockSchoolId, function(delegates) {
      calls++;
      expect($.ajax).toBeCalledWith({
        type: 'GET',
        url: '/api/schools/' + mockSchoolId + '/delegates',
        dataType: 'json',
        success: jasmine.any(Function),
      });
      expect(delegates).toEqual(mockDelegates);
    });
    jest.runAllTimers();

    DelegateStore.getDelegates(mockSchoolId, function(delegates) {
      calls++;
      expect($.ajax.mock.calls.length).toBe(1);
      expect(delegates).toEqual(mockDelegates);
    });
    jest.runAllTimers();

    expect(calls).toBe(2);
  });
});
