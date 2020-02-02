/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

 'use strict';

 /**
 * Inflates grades by 5/10. 
 */
function inflateGrade(grade) {
    if (grade === 0) {
        return 0;
    }
    return (grade / 2) + 5;
  }
  
  module.exports = inflateGrade;
  