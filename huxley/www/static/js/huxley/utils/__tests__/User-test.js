/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../User');

describe('User', function() {
  var User;

  beforeEach(function() {
    User = require('../User');
  });

  it('instantiates an anonymous user', function() {
    var user = {};

    expect(User.isAnonymous(user)).toBe(true);
    expect(User.isAdvisor(user)).toBe(false);
    expect(User.isChair(user)).toBe(false);
  });

  it('instantiates an advisor', function() {
    var user = {id: 1, user_type: 1};

    expect(User.isAnonymous(user)).toBe(false);
    expect(User.isAdvisor(user)).toBe(true);
    expect(User.isChair(user)).toBe(false);
  });

  it('instantiates a chair', function() {
    var user = {id: 1, user_type: 2};

    expect(User.isAnonymous(user)).toBe(false);
    expect(User.isAdvisor(user)).toBe(false);
    expect(User.isChair(user)).toBe(true);
  });
});
