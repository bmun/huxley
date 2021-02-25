/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import PropTypes from "prop-types";

let ConferenceContext = {
  session: PropTypes.number,
  start_date: PropTypes.shape({
    month: PropTypes.string,
    day: PropTypes.string,
    year: PropTypes.string,
  }),
  end_date: PropTypes.shape({
    month: PropTypes.string,
    day: PropTypes.string,
    year: PropTypes.string,
  }),
  reg_open: PropTypes.string,
  round_one_end: PropTypes.string,
  round_two_fees_due: PropTypes.string,
  round_two_start: PropTypes.string,
  round_two_end: PropTypes.string,
  round_two_fees_due: PropTypes.string,
  round_three_start: PropTypes.string,
  round_three_end: PropTypes.string,
  round_four_start: PropTypes.string,
  round_three_fees_due: PropTypes.string,
  reg_close: PropTypes.string,
  round_four_fees_due: PropTypes.string,
  part_refund_deadline: PropTypes.string,
  early_paper_deadline: PropTypes.shape({
    month: PropTypes.string,
    day: PropTypes.string,
  }),
  paper_deadline: PropTypes.shape({
    month: PropTypes.string,
    day: PropTypes.string,
  }),
  waiver_avail_date: PropTypes.string,
  waiver_deadlines: PropTypes.string,
  waiver_link: PropTypes.string,
  external: PropTypes.string,
  treasurer: PropTypes.string,
  registration_fee: PropTypes.number,
  delegate_fee: PropTypes.number,
  registration_open: PropTypes.bool,
  registration_waitlist: PropTypes.bool,
  position_papers_accepted: PropTypes.bool,
};

export { ConferenceContext };
