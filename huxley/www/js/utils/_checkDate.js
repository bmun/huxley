/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

/**
 * Checks if the current date falls within the range of February 28th to March 31st
 */
function _checkDate() {
  const date = new Date();
  const advisorDeadline = Date.parse(global.conference.advisor_edit_deadline)

  return (date.getTime() >= advisorDeadline);
}

export { _checkDate };
