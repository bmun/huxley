/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

/**
 * Inflates grades by 50%.
 */
function inflateGrades(grade, total) {
  if (grade === 0) {
    return 0;
  }
  return Math.min(grade + total / 2.6, total);
}

export { inflateGrades };
