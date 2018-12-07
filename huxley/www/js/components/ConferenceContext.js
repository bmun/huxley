/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

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
  external: React.PropTypes.string,
  registration_fee: React.PropTypes.number,
  delegate_fee: React.PropTypes.number,
  registration_open: React.PropTypes.bool,
  registration_waitlist: React.PropTypes.bool,
  position_papers_accepted: React.PropTypes.bool,
};

module.exports = ConferenceContext;
