/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

/*
 * General purpose safe object accessing function
 */
var _accessSafe = function(obj, key) {
  return obj && obj[key];
};

module.exports = _accessSafe;
