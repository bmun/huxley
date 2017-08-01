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
    attendance: React.PropTypes.array
  },

  render() {
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
              checked={this.props.attendance[0]}
              onChange={this._handleChange.bind(this, 0)}
            />
          </label>
        </td>
        <td>
          <label name="session">
            <input
              className="choice"
              type="checkbox"
              checked={this.props.attendance[1]}
              onChange={this._handleChange.bind(this, 1)}
            />
          </label>
        </td>
        <td>
          <label name="session">
            <input
              className="choice"
              type="checkbox"
              checked={this.props.attendance[2]}
              onChange={this._handleChange.bind(this, 2)}
            />
          </label>
        </td>
        <td>
          <label name="session">
            <input
              className="choice"
              type="checkbox"
              checked={this.props.attendance[3]}
              onChange={this._handleChange.bind(this, 3)}
            />
          </label>
        </td>
        <td>
          <label name="session">
            <input
              className="choice"
              type="checkbox"
              checked={this.props.attendance[4]}
              onChange={this._handleChange.bind(this, 4)}
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
