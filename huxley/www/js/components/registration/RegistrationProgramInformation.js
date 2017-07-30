/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var ProgramTypes = require('constants/ProgramTypes');
var NumberInput = require('components/NumberInput');
var _accessSafe = require('utils/_accessSafe');

const RegistrationProgramInformation = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object,
    errors: React.PropTypes.object,
    programInformation: React.PropTypes.object,
    handleProgramTypeChange: React.PropTypes.func,
    programType: React.PropTypes.oneOf([ProgramTypes.CLUB, ProgramTypes.CLASS]),
  },

  shouldComponentUpdate: function(nextProps, nextState) {
    for (let key in this.props.programInformation) {
      if (
        this.props.programInformation[key] !== nextProps.programInformation[key]
      ) {
        return true;
      }
    }
    return this.props.programType !== nextProps.programType;
  },

  render: function() {
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    var accessProgram = _accessSafe.bind(this, this.props.programInformation);
    return (
      <div id="program_information">
        <h3>Program Information</h3>
        <p className="instructions">
          What category best describes your program?
        </p>
        <ul>
          <li>
            <label>
              <input
                type="radio"
                checked={this.props.programType == ProgramTypes.CLUB}
                value={ProgramTypes.CLUB}
                onChange={this.props.handleProgramTypeChange}
              />{' '}
              Club
            </label>
          </li>
          <li>
            <label>
              <input
                type="radio"
                value={ProgramTypes.CLASS}
                checked={this.props.propTypes == ProgramTypes.CLASS}
                onChange={this.props.handleProgramTypeChange}
              />{' '}
              Class
            </label>
          </li>
        </ul>
        <p className="instructions">
          Please tell us a bit more about your delegation this year. Provide us
          with the tentative number of beginner, intermediate, and advanced
          delegates you intend to bring to BMUN. Try to provide us with
          realistic estimates for your delegate numbers in each category so we
          can provide your delegation with the appropriate number and type of
          assignments.
        </p>
        <NumberInput
          placeholder="Number of BMUN sessions attended"
          onChange={accessHandlers('times_attended')}
          value={accessProgram('times_attended')}
        />
        {accessErrors('times_attended')}
        <NumberInput
          placeholder="Tentative Number of Beginner Delegates"
          onChange={accessHandlers('beginner_delegates')}
          value={accessProgram('beginner_delegates')}
        />
        <label className="hint">
          Beginner: Attended 0-3 conferences, not very familiar with Model
          United Nations.
        </label>
        {accessErrors('beginner_delegates')}
        <NumberInput
          placeholder="Tentative Number of Intermediate Delegates"
          onChange={accessHandlers('intermediate_delegates')}
          value={accessProgram('intermediate_delegates')}
        />
        <label className="hint">
          Intermediate: Attended 4-7 conferences, little to no practice in
          advanced committees.
        </label>
        {accessErrors('intermediate_delegates')}
        <NumberInput
          placeholder="Tentative Number of Advanced Delegates"
          onChange={accessHandlers('advanced_delegates')}
          value={accessProgram('advanced_delegates')}
        />
        <label className="hint">
          Advanced: Attended more than seven conferences, has participated in
          many diverse committees.
        </label>
        {accessErrors('advanced_delegates')}
        <p className="instructions">
          Tentative Total Number of Delegates:{' '}
          {this._handleDelegateSum(
            accessProgram('beginner_delegates'),
            accessProgram('intermediate_delegates'),
            accessProgram('advanced_delegates'),
          )}
        </p>
      </div>
    );
  },

  _handleDelegateSum: function(beginner, intermediate, advanced) {
    var sum = 0;
    if (beginner) {
      sum += parseInt(beginner, 10) || 0;
    }
    if (intermediate) {
      sum += parseInt(intermediate, 10) || 0;
    }
    if (advanced) {
      sum += parseInt(advanced, 10) || 0;
    }
    return sum;
  },
});

module.exports = RegistrationProgramInformation;
