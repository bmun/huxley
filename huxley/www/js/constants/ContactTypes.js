/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var invariant = require('fbjs/lib/invariant');

invariant(
  global.ContactTypes !== undefined,
  'global.ContactTypes must be defined.',
);

var ContactTypes = global.ContactTypes;
delete global.ContactTypes;

module.exports = ContactTypes;
