/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

 'use strict';

 /**
 * Inflates grades by 50%. 
 */
function inflateGrade(grade, total) {
    if (grade === 0) {
        return 0;
    }
    return (grade / 2) + (total / 2);
  }
  
  module.exports = inflateGrade;
  