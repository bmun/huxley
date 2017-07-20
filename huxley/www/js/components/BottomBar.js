/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var cx = require('classnames');
var React = require('react');


require('css/BottomBar.less');

var BottomBar = React.createClass({
  render: function() {
    return (
      <div>
        <div className="bottom-bar">
          <span className="grey-text"> Having Issues?</span>
          &nbsp;
          &nbsp;
          <span>
          <a className="support-link" href="mailto:tech@bmun.org?subject=Issues%20With%20Huxley">Email Us</a>
          </span>
        </div>
      </div>
    );
  },
});

module.exports = BottomBar;
