/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../CurrentUserStore')

describe('CurrentUserStore', function() {
  var $;
  var CurrentUserStore;
  var User;

  var mockCurrentUser;

  beforeEach(function() {
    $ = require('jquery');
    CurrentUserStore = require('../CurrentUserStore');
    User = require('../../User');

    currentUser = new User({
      id: 1,
      first_name: 'test',
      last_name: 'user',
      user_type: 1
    });
    mockCurrentUser = currentUser;
    CurrentUserStore.bootstrap()
  });

  it('requests the current user on first call and caches locally', function() {
    var user = CurrentUserStore.getCurrentUser();
    expect(user.id).toEqual(mockCurrentUser.id);
    expect(user.first_name).toEqual(mockCurrentUser.first_name);
    expect(user.last_name).toEqual(mockCurrentUser.last_name);
    expect(user.user_type).toEqual(mockCurrentUser.user_type);
  });
});
