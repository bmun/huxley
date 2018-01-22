/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var Button = require('components/core/Button')

var React = require('react');

var PaperAssignmentList = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    assignments: React.PropTypes.array,
    countries: React.PropTypes.object
  },

  render() {
    var assignments = this.props.assignments;
    var countries = this.props.countries;
    var rows = assignments.map(a => {
      var buttonCell = a.paper.file != null ? <Button
                                                color="green"
                                                onClick={this._handleChange.bind(this, a.id)}>
                                                Grade
                                              </Button> :
                                              <div>No paper submitted.</div>
      return (
        <tr key={a.id}>
          <td>
            {countries[a.country].name}
          </td>
          <td>
            {buttonCell}
          </td>
        </tr>
      )
    });

    return (
      <table>
        <thead>
          <tr>
            <th>Country</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    )
  },

  _handleChange: function(assignmentID, event) {
    this.props.onChange &&
      this.props.onChange(assignmentID, event);
  },
});

module.exports = PaperAssignmentList;