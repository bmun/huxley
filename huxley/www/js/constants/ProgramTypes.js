/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import invariant from "invariant";

invariant(
  global.ProgramTypes !== undefined,
  "global.ProgramTypes must be defined."
);

var ProgramTypes = global.ProgramTypes;
delete global.ProgramTypes;

export default ProgramTypes;
