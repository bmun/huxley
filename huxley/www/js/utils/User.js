/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

var TYPE_ADVISOR = 1;
var TYPE_CHAIR = 2;
var TYPE_DELEGATE = 3;

var User = {
  isAnonymous(user) {
    return user ? !user.id : true;
  },

  isAdvisor(user) {
    return user.user_type == TYPE_ADVISOR;
  },

  isChair(user) {
    return user.user_type == TYPE_CHAIR;
  },

  isDelegate(user) {
    return user.user_type == TYPE_DELEGATE;
  },

  getSchool(user) {
    return user.school || {};
  },
};

export { User };
