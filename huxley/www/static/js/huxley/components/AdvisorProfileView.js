/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var React = require('react');

var Button = require('./Button');
var InnerView = require('./InnerView');
var LogoutButton = require('./LogoutButton');
var ConferenceContext = require('./ConferenceContext');
var PhoneInput = require('./PhoneInput');
var ProgramTypes = require('../constants/ProgramTypes');
var User = require('../utils/User');

require('jquery-ui/effect-shake');

var AdvisorProfileView = React.createClass({

  // #489
  // The below code was commented out due to
  // https://github.com/reactjs/react-router/blob/master/upgrade-guides/v1.0.0.md#routehandler
  // see the last section. I am wary to remove for fear that we won't validate
  // propTypes: {
  //   user: React.PropTypes.object.isRequired
  // },

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  getInitialState: function() {
    var user = this.props.user;
    var school = User.getSchool(user);
    return {
      errors: {},
      first_name: user.first_name,
      last_name: user.last_name,
      school_name: school.name,
      school_address: school.address,
      school_city: school.city,
      school_zip_code: school.zip_code,
      primary_name: school.primary_name,
      primary_email: school.primary_email,
      primary_phone: school.primary_phone,
      secondary_name: school.secondary_name,
      secondary_email: school.secondary_email,
      secondary_phone: school.secondary_phone
    }
  },

  render: function() {
    var conference = this.context.conference;
    var user = this.props.user;
    var school = User.getSchool(user);
    var invoiceUrl = '/api/schools/' + school.id + '/invoice/';
    return (
      <InnerView>
        <h2>Welcome, {user.first_name}!</h2>
        <p>
          We are very excited to see {school.name} at BMUN {conference.session} this year! Here,
          you can view your registration information for the conference. Please
          note that fees are currently <strong>estimates</strong> based on the
          approximate delegation size given during registration.
        </p>
        <br />
        <p>
          Advisors, if you wish to generate an invoice for your school with your
          payment details, please click on the Generate Your Invoice button under
          the Fees tab. You will receive an invoice in your email within 2 business
          days.
        </p>
        <br />
        <p><strong>Important Note:</strong> Please mail all checks to <strong>
        P.O. Box 4306 Berkeley, CA 94704-0306. If you have any other further
        questions contact me at <a href="mailto:info@bmun.org">
        info@bmun.org</a> and I will respond to all requests efficiently.
        See you soon!</strong></p>
        <br />
        <p><strong>{conference.external}
        <br />
        Under-Secretary General of External Relations, {conference.session}th Session.</strong></p>
        <form 
          id="welcomepage" 
          onSubmit={this._handleSubmit}>
          <div className="tablemenu header">
          </div>
          <div id="welcomeinfocontainer" className="table-container">
            <table id="welcomeinfo" className="table highlight-cells">
              <thead>
                <tr>
                  <th colSpan="2">Advisor Information</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="fieldLabel">First Name</td>
                  <td className="field">
                    <input
                      type="text"
                      value={this.state.first_name}
                      onChange={this._handleChange.bind(this, 'first_name')}
                    />
                    {this.renderError('first_name')}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Last Name</td>
                  <td className="field">
                    <input
                      type="text"
                      value={this.state.last_name}
                      onChange={this._handleChange.bind(this, 'last_name')}
                    />
                    {this.renderError('last_name')}
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">School Information</th>
                </tr>
                <tr>
                  <td className="fieldLabel">Name</td>
                  <td className="field">
                    {school.name}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Address</td>
                  <td className="field">
                    <input
                      type="text"
                      value={this.state.school_address}
                      onChange={this._handleChange.bind(this, 'school_address')}
                    />
                    {this.renderError('address')}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">City</td>
                  <td className="field">
                    <input
                      type="text"
                      value={this.state.school_city}
                      onChange={this._handleChange.bind(this, 'school_city')}
                    />
                    {this.renderError('city')}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Zip</td>
                  <td className="field">
                    <input
                      type="text"
                      value={this.state.school_zip_code}
                      onChange={this._handleChange.bind(this, 'school_zip_code')}
                    />
                    {this.renderError('zip_code')}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Waitlisted</td>
                  <td className="field">
                    {school.waitlist == true ? 'Yes' : 'No'}
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">Program Information</th>
                </tr>
                <tr>
                  <td className="fieldLabel">Program Type</td>
                  <td className="field">
                    {school.program_type === 1 ? 'Club' : 'Class'}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Times Attended</td>
                  <td className="field">
                    {school.times_attended}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Number of Beginner Delegates</td>
                  <td className="field">
                    {school.beginner_delegates}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Number of Intermediate Delegates</td>
                  <td className="field">
                    {school.intermediate_delegates}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Number of Advanced Delegates</td>
                  <td className="field">
                    {school.advanced_delegates}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Number of Spanish Speaking
                  Delegates</td>
                  <td className="field">
                    {school.spanish_speaking_delegates}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Number of Chinese Speaking
                  Delegates</td>
                  <td className="field">
                    {school.chinese_speaking_delegates}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Waivers Completed?</td>
                  <td className="field">
                    {school.waivers_completed ? "Yes" : "No"}
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">Primary Contact Information</th>
                </tr>
                <tr>
                  <td className="fieldLabel">Name</td>
                  <td className="field">
                    <input
                      type="text"
                      value={this.state.primary_name}
                      onChange={this._handleChange.bind(this, 'primary_name')}
                    />
                    {this.renderError('primary_name')}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Email</td>
                  <td className="field">
                    <input
                      type="text"
                      value={this.state.primary_email}
                      onChange={this._handleChange.bind(this, 'primary_email')}
                    />
                    {this.renderError('primary_email')}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Phone</td>
                  <td className="field">
                    <PhoneInput
                      value={this.state.primary_phone}
                      isInternational={school.international}
                      id="primary_phone"
                      onChange={this._handleChange.bind(this, 'primary_phone')}
                    />
                    {this.renderError('primary_phone')}
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">Secondary Contact Information</th>
                </tr>
                <tr>
                  <td className="fieldLabel">Name</td>
                  <td className="field">
                    <input
                      type="text"
                      value={this.state.secondary_name}
                      id="secondary_name"
                      onChange={this._handleChange.bind(this, 'secondary_name')}
                    />
                    {this.renderError('secondary_name')}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Email</td>
                  <td className="field">
                    <input
                      type="text"
                      value={this.state.secondary_email}
                      onChange={this._handleChange.bind(this, 'secondary_email')}
                    />
                    {this.renderError('secondary_email')}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Phone</td>
                  <td className="field">
                    <PhoneInput
                      value={this.state.secondary_phone}
                      isInternational={school.international}
                      id="secondary_phone"
                      onChange={this._handleChange.bind(this, 'secondary_phone')}
                    />
                    {this.renderError('secondary_phone')}
                  </td>
                </tr>
                <tr>
                  <th>Fees</th>
                  <td className="field">
                    <a className="button button-green" href={invoiceUrl} target="_blank">
                      Generate Your Invoice
                    </a>
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Fees Owed</td>
                  <td className="field">
                    {'$' + school.fees_owed.toFixed(2)}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Fees Paid</td>
                  <td className="field">
                    {'$' + school.fees_paid.toFixed(2)}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Balance</td>
                  <td className="field">
                    {'$' + (school.fees_owed - school.fees_paid).toFixed(2)}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="tablemenu footer">
          </div>
          <Button
            color="green"
            loading={this.state.loading}
            type="submit">
            Save
          </Button>
          <span className="help-text"><em> Remember to save any changes!</em></span>
        </form>
      </InnerView>
    );
  },

  renderError: function(field) {
    if (this.state.errors[field]) {
      return (
        <label className="hint error">
          {this.state.errors[field]}
        </label>
      );
    }

    if (this.state.errors.school &&
        this.state.errors.school[field]) {
      return (
        <label className="hint error">
          {this.state.errors.school[field]}
        </label>
      );
    }

    return null;
  },

  _handleChange: function(fieldName, event) {
    var change = {};

    // Handles both changes from HTMl and custom components
    if (event.target) {
      change[fieldName] = event.target.value;
    } else {
      change[fieldName] = event
    }

    this.setState(change);
  },

  _handleSubmit: function(event) {
    var user = this.props.user;
    var currentDate = new Date();
    this.setState({loading: true});
    $.ajax({
      type: 'PATCH',
      url: '/api/users/' + user.id,
      data: JSON.stringify({
        first_name: this.state.first_name.trim(),
        last_name: this.state.last_name.trim(),
        school: {
          address: this.state.school_address.trim(),
          city: this.state.school_city.trim(),
          zip_code: this.state.school_zip_code.trim(),
          primary_name: this.state.primary_name.trim(),
          primary_email: this.state.primary_email.trim(),
          primary_phone: this.state.primary_phone.trim(),
          secondary_name: this.state.secondary_name.trim(),
          secondary_email: this.state.secondary_email.trim(),
          secondary_phone: this.state.secondary_phone.trim(),
          modified: currentDate
        }
      }),
      success: this._handleSuccess,
      error: this._handleError,
      contentType: 'application/json'
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    this.setState({
      errors: {},
      loading: false
    }, this.onSuccess);
  },

  _handleError: function(jqXHR, status, error) {
    var response = jqXHR.responseJSON;
    if (!response) {
      return;
    }

    this.setState({
      errors: response,
      loading: false
    }, function() {
      $('#huxley-app').effect(
        'shake',
        {direction: 'up', times: 2},
        250
      );
    });
  }
});
module.exports = AdvisorProfileView;
