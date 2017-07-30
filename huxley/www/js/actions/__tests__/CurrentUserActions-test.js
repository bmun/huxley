/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('actions/CurrentUserActions');

describe('CurrentUserActions', function() {
  var ActionConstants;
  var CurrentUserActions;
  var Dispatcher;

  beforeEach(function() {
    ActionConstants = require('constants/ActionConstants');
    CurrentUserActions = require('actions/CurrentUserActions');
    Dispatcher = require('dispatcher/Dispatcher');
  });

  it('dispatches the login action', function() {
    var user = {id: 1, first_name: 'Mike', last_name: 'Jones'};
    CurrentUserActions.login(user);

    expect(Dispatcher.dispatch.mock.calls.length).toBe(1);
    expect(Dispatcher.dispatch).toBeCalledWith({
      actionType: ActionConstants.LOGIN,
      user: user,
    });
  });

  it('dispatches the logout action', function() {
    CurrentUserActions.logout();

    expect(Dispatcher.dispatch.mock.calls.length).toBe(1);
    expect(Dispatcher.dispatch).toBeCalledWith({
      actionType: ActionConstants.LOGOUT,
    });
  });
});
