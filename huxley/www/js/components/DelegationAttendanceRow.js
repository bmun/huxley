/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var DelegationAttendanceRow = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    countryName: React.PropTypes.string,
    assignmentID: React.PropTypes.number,
    attendance: React.PropTypes.object
  },

  shouldComponentUpdate(nextProps, nextState) {
    for (var field in this.props.attendance) {
      if (this.props.attendance[field] !== nextProps.attendance[field]){
        return true;
      }
    }
    return this.props.countryName !== nextProps.countryName;
  },

  render() {
    console.log(this.props.assignmentID);
    return (
      <tr>
        <td>
          {this.props.countryName}
        </td>
        <td>
          <label name="session">
            <input
              className="choice"
              type="checkbox"
              checked={this.props.attendance["voting"]}
              onChange={this._handleChange.bind(this, "voting")}
            />
          </label>
        </td>
        <td>
          <label name="session">
            <input
              className="choice"
              type="checkbox"
              checked={this.props.attendance["session_one"]}
              onChange={this._handleChange.bind(this, "session_one")}
            />
          </label>
        </td>
        <td>
          <label name="session">
            <input
              className="choice"
              type="checkbox"
              checked={this.props.attendance["session_two"]}
              onChange={this._handleChange.bind(this, "session_two")}
            />
          </label>
        </td>
        <td>
          <label name="session">
            <input
              className="choice"
              type="checkbox"
              checked={this.props.attendance["session_three"]}
              onChange={this._handleChange.bind(this, "session_three")}
            />
          </label>
        </td>
        <td>
          <label name="session">
            <input
              className="choice"
              type="checkbox"
              checked={this.props.attendance["session_four"]}
              onChange={this._handleChange.bind(this, "session_four")}
            />
          </label>
        </td>
      </tr>
    );
  },

  _handleChange: function(field, event) {
    this.props.onChange &&
      this.props.onChange(field, this.props.countryID, event);
  },
});

module.exports = DelegationAttendanceRow;
