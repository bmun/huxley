/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var mergeInto = require('react/lib/mergeInto');

var TYPE_ADVISOR = 1;
var TYPE_CHAIR = 2;

function User(rawData) {
  this._user = rawData || {};
}

mergeInto(User.prototype, {
  isAnonymous: function() {
    return !this._user.id;
  },

  isAdvisor: function() {
    return this._user.user_type == TYPE_ADVISOR;
  },

  isChair: function() {
    return this._user.user_type == TYPE_CHAIR;
  },

  destroy: function() {
    delete this._user;
  }
});

module.exports = User;
