/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../CurrentUserStore')

describe('CurrentUserStore', function() {
  var CurrentUserStore;
  var User;

  beforeEach(function() {
    CurrentUserStore = require('../CurrentUserStore');
    User = require('../../User');
  });

  it('deletes the reference to the global user object', function() {
    global.currentUser = new User({
      user_type: 1
    });
    CurrentUserStore.bootstrap()
    expect(global.currentUser).toBeUndefined();
  });
});
