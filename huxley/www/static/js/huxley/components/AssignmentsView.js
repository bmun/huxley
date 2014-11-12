/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');
var AdvisorView = require('./AdvisorView');

var AssignmentsView = React.createClass({
  render: function(){
    return(
      <AdvisorView user={this.props.user}>
      </AdvisorView>
    );
  }
});

module.exports = AssignmentsView;
