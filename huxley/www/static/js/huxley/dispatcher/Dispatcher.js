/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var _callbacks = [];

var Dispatcher = {
  register: function(callback) {
    _callbacks.push(callback);
    return _callbacks.length - 1;
  },

  dispatch: function(action) {
    _callbacks.forEach(function(callback) {
      callback(action);
    });
  }
};

module.exports = Dispatcher;
