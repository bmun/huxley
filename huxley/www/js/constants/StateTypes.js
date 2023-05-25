/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import invariant from "invariant";

invariant(
  global.StateTypes !== undefined,
  "global.StateTypes must be defined."
);

var StateTypes = global.StateTypes;
delete global.StateTypes;

export { StateTypes };
