/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import React from 'react';

var ConferenceContext = {
  session: React.PropTypes.number,
  start_date: React.PropTypes.shape({
    month: React.PropTypes.string,
    day: React.PropTypes.string,
    year: React.PropTypes.string,
  }),
  end_date: React.PropTypes.shape({
    month: React.PropTypes.string,
    day: React.PropTypes.string,
    year: React.PropTypes.string,
  }),
  reg_open: React.PropTypes.string,
  round_one_end: React.PropTypes.string,
  round_two_fees_due: React.PropTypes.string,
  round_two_start: React.PropTypes.string,
  round_two_end: React.PropTypes.string,
  round_two_fees_due: React.PropTypes.string,
  round_three_start: React.PropTypes.string,
  round_three_end: React.PropTypes.string,
  round_four_start: React.PropTypes.string,
  round_three_fees_due: React.PropTypes.string,
  reg_close: React.PropTypes.string,
  round_four_fees_due: React.PropTypes.string,
  part_refund_deadline: React.PropTypes.string,
  early_paper_deadline: React.PropTypes.shape({
    month: React.PropTypes.string,
    day: React.PropTypes.string,
  }),
  paper_deadline: React.PropTypes.shape({
    month: React.PropTypes.string,
    day: React.PropTypes.string,
  }),
  waiver_avail_date: React.PropTypes.string,
  waiver_deadlines: React.PropTypes.string,
  waiver_link: React.PropTypes.string,
  external: React.PropTypes.string,
  treasurer: React.PropTypes.string,
  registration_fee: React.PropTypes.number,
  delegate_fee: React.PropTypes.number,
  registration_open: React.PropTypes.bool,
  registration_waitlist: React.PropTypes.bool,
  position_papers_accepted: React.PropTypes.bool,
};

module.exports = ConferenceContext;
