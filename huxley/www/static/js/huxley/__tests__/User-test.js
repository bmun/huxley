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
    var user = new User();

    expect(user.isAnonymous()).toBe(true);
    expect(user.isAdvisor()).toBe(false);
    expect(user.isChair()).toBe(false);
  });

  it('instantiates an advisor', function() {
    var user = new User({id: 1, user_type: 1});

    expect(user.isAnonymous()).toBe(false);
    expect(user.isAdvisor()).toBe(true);
    expect(user.isChair()).toBe(false);
  });

  it('instantiates a chair', function() {
    var user = new User({id: 1, user_type: 2});

    expect(user.isAnonymous()).toBe(false);
    expect(user.isAdvisor()).toBe(false);
    expect(user.isChair()).toBe(true);
  });

  it('becomes unusable after destruction', function() {
    var user = new User();
    user.destroy();

    expect(function() { user.isAnonymous(); }).toThrow();
    expect(function() { user.isAdvisor(); }).toThrow();
    expect(function() { user.isChair(); }).toThrow();
  });
});
