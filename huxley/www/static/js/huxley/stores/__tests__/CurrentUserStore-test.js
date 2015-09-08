/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../CurrentUserStore');

describe('CurrentUserStore', function() {
  var ActionConstants;
  var CurrentUserStore;
  var Dispatcher;

  var registerCallback;

  beforeEach(function() {
    ActionConstants = require('../../constants/ActionConstants');
    CurrentUserStore = require('../CurrentUserStore');
    Dispatcher = require('../../dispatcher/Dispatcher');

    registerCallback = function(action) {
      Dispatcher.isDispatching.mockReturnValue(true);
      Dispatcher.register.mock.calls[0][0](action);
      Dispatcher.isDispatching.mockReturnValue(false);
    };
    global.currentUser = {id: 1, user_type: 1};

    registerCallback({
      actionType: ActionConstants.BOOTSTRAP,
    });
  });

  it('correctly bootstraps the current user object', function() {
    expect(CurrentUserStore.getCurrentUser()).not.toBeUndefined();
  });

  it('deletes the reference to the global user object', function() {
    expect(global.currentUser).toBeUndefined();
  });

  it('subscribes to the dispatcher', function() {
    expect(Dispatcher.register).toBeCalled();
  });

  it('sets a new user on login', function() {
    var user = CurrentUserStore.getCurrentUser();
    registerCallback({
      actionType: ActionConstants.LOGIN,
      user: {id: 2, user_type: 1}
    });
    var mockUser = CurrentUserStore.getCurrentUser();
    expect(user).not.toBe(mockUser);
    expect(mockUser.id).toEqual(2);
    expect(mockUser.user_type).toEqual(1);
  });

  it('sets an anonymous user on logout', function() {
    registerCallback({
      actionType: ActionConstants.LOGOUT,
    });
    var mockUser = CurrentUserStore.getCurrentUser();
    expect(mockUser).toEqual({});
  });

  it('emits a change when the user changes', function() {
    var callback = jest.genMockFunction();
    CurrentUserStore.addListener(callback);
    expect(callback).not.toBeCalled();
    registerCallback({
      actionType: ActionConstants.LOGIN,
      user: {id: 1, user_type: 1}
    });
    expect(callback).toBeCalled();
  });
});
