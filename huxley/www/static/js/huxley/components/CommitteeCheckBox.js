/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var CommitteeCheckBox = React.createClass({
  render: function() {
    return (
      <input
        className="choice"
        type="checkbox"
        name="committee_prefs"
        //onChange={this._handleCommitteePreferenceChange}
      />
    );
  }
});
module.exports = CommitteeCheckBox;
