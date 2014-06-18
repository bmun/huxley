/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../CurrentUserStore')
jest.dontMock('../../dispatcher/Dispatcher')
jest.dontMock('../../actions/CurrentUserActions')
jest.dontMock('../../User');

describe('CurrentUserStore', function() {
  var CurrentUserStore;
  var User;
  var Dispatcher;
  var CurrentUserActions;

  beforeEach(function() {
    CurrentUserStore = require('../CurrentUserStore');
    User = require('../../User');
    Dispatcher = require('../../dispatcher/Dispatcher');
    CurrentUserActions = require('../../actions/CurrentUserActions');
    global.currentUser = {id: 1, user_type: 1};
    CurrentUserStore.bootstrap();
  });

  it('correctly bootstraps the current user object', function() {
    expect(CurrentUserStore.getCurrentUser()).not.toBeUndefined();
  })

  it('deletes the reference to the global user object', function() {
    expect(global.currentUser).toBeUndefined();
  });

  it('sets a new user on login', function() {
    var user = CurrentUserStore.getCurrentUser();
    CurrentUserActions.login(user.getData());
    var mockUser = CurrentUserStore.getCurrentUser();
    expect(user).not.toBe(mockUser);
  });

  it('sets an anonymous user on logout', function() {
    CurrentUserActions.logout();
    var mockUser = CurrentUserStore.getCurrentUser();
    expect(mockUser.isAnonymous()).toBeTruthy();
  })
});
