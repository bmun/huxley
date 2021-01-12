/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/CurrentUserStore');

describe('CurrentUserStore', function() {
  var ActionConstants;
  var CurrentUserStore;
  var Dispatcher;
  var ServerAPI;

  var registerCallback;

  beforeEach(function() {
    ActionConstants = require('constants/ActionConstants');
    {CurrentUserStore} = require('stores/CurrentUserStore');
    Dispatcher = require('dispatcher/Dispatcher');
    ServerAPI = require('lib/ServerAPI');

    registerCallback = function(action) {
      Dispatcher.isDispatching.mockReturnValue(true);
      Dispatcher.register.mock.calls[0][0](action);
      Dispatcher.isDispatching.mockReturnValue(false);
    };
    global.currentUser = {id: 1, user_type: 1};

    registerCallback({
      actionType: ActionConstants.BOOTSTRAP,
    });

    ServerAPI.updateSchool.mockReturnValue(Promise.resolve({}));
    ServerAPI.updateUser.mockReturnValue(Promise.resolve({}));
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
      user: {id: 2, user_type: 1},
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
      user: {id: 1, user_type: 1},
    });
    expect(callback).toBeCalled();
  });

  it('updates the school of a user and emits a change', function() {
    registerCallback({
      actionType: ActionConstants.LOGIN,
      user: {id: 2, user_type: 1, school: {id: 1}},
    });
    var mockUser = CurrentUserStore.getCurrentUser();

    var callback = jest.genMockFunction();
    CurrentUserStore.addListener(callback);
    expect(callback).not.toBeCalled();

    var delta = {name: 'School', assignments_finalized: true};
    registerCallback({
      actionType: ActionConstants.UPDATE_SCHOOL,
      schoolID: 1,
      delta: delta,
    });
    expect(callback).toBeCalled();
    expect(ServerAPI.updateSchool).toBeCalledWith(1, delta);

    mockUser = CurrentUserStore.getCurrentUser();
    expect(mockUser.school.name).toEqual(delta.name);
    expect(mockUser.school.assignments_finalized).toBe(true);
  });

  it('updates a user and emits a change', function() {
    registerCallback({
      actionType: ActionConstants.LOGIN,
      user: {
        id: 2,
        user_type: 1,
        first_name: 'Trevor',
        last_name: 'Dowds',
        school: {
          address: '1 School Way',
          city: 'School City',
          zip_code: '123456',
          primary_name: 'Trevor',
          primary_email: 't@d.com',
          primary_phone: '123456789',
          secondary_name: '',
          secondary_email: '',
          secondary_phone: '',
        },
      },
    });
    var mockUser = CurrentUserStore.getCurrentUser();

    var callback = jest.genMockFunction();
    CurrentUserStore.addListener(callback);
    expect(callback).not.toBeCalled();

    var delta = {
      first_name: 'Trev',
      last_name: 'Dowds',
      school: {
        address: '1 School Way',
        city: 'School City',
        zip_code: '123456',
        primary_name: 'Trevor',
        primary_email: 'trev@d.com',
        primary_phone: '123456789',
        secondary_name: '',
        secondary_email: '',
        secondary_phone: '',
      },
    };
    registerCallback({
      actionType: ActionConstants.UPDATE_USER,
      userID: 2,
      delta: delta,
    });
    expect(callback).toBeCalled();

    mockUser = CurrentUserStore.getCurrentUser();
    expect(mockUser.first_name).toEqual(delta.first_name);
    expect(mockUser.last_name).toEqual(delta.last_name);
    expect(mockUser.school).toEqual(delta.school);
  });
});
