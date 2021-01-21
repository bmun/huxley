/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import invariant from "invariant";

invariant(
  global.GenderConstants !== undefined,
  "global.GenderConstants must be defined."
);

var GenderConstants = global.GenderConstants;
delete global.GenderConstants;

export { GenderConstants };
