/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var cx = require('classnames');
var React = require('react');

require('css/SupportLink.less');

var SupportLink = React.createClass({
  render: function() {
    return (
      <div className="link-wrapper">
        <span className="grey-text">Having Issues?</span>
        &nbsp;
        &nbsp;
        <span>
          <a
            className="mailto-link"
            href="mailto:tech@bmun.org?subject=Issues%20With%20Huxley">
            Email Us
          </a>
        </span>
      </div>
    );
  },
});

module.exports = SupportLink;