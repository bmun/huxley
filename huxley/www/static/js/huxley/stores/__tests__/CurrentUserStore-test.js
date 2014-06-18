/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../CurrentUserStore');
jest.dontMock('../../User');
jest.dontMock('events');

describe('CurrentUserStore', function() {
  var ActionConstants;
  var CurrentUserStore;
  var Dispatcher;

  var registerCallback;

  beforeEach(function() {
    ActionConstants = require('../../constants/ActionConstants');
    CurrentUserStore = require('../CurrentUserStore');
    Dispatcher = require('../../dispatcher/Dispatcher');

    registerCallback = Dispatcher.register.mock.calls[0][0];
    global.currentUser = {id: 1, user_type: 1};
    CurrentUserStore.bootstrap();
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
      user: {id: 1, user_type: 1}
    });
    var mockUser = CurrentUserStore.getCurrentUser();
    expect(user).not.toBe(mockUser);
    expect(mockUser.getData().id).toEqual(1);
    expect(mockUser.getData().user_type).toEqual(1);
  });

  it('sets an anonymous user on logout', function() {
    registerCallback({
      actionType: ActionConstants.LOGOUT,
    });
    var mockUser = CurrentUserStore.getCurrentUser();
    expect(mockUser.isAnonymous()).toBe(true);
  });

  it('emits a change when the user changes', function() {
    var callback = jest.genMockFunction();
    CurrentUserStore.addChangeListener(callback);
    expect(callback).not.toBeCalled();
    registerCallback({
      actionType: ActionConstants.LOGIN,
      user: {id: 1, user_type: 1}
    });
    expect(callback).toBeCalled();
  });
});
