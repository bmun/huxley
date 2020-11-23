/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

/**
 * Checks if the current date falls within the range of February 28th to March 31st
 */
function _checkDate() {
  var date = new Date();
  console.log(date.getMonth());
  return (
    (date.getDate() >= 28 && date.getMonth() == 1) ||
    (date.getDate() <= 31 && date.getMonth() == 2)
  );
}

module.exports = _checkDate;
