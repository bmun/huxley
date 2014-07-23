/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var console = require('console');

var $ = require('jquery');
var React = require('react/addons');
var RRouter = require('rrouter');

var Button = require('./Button');
var ContactTypes = require('../constants/ContactTypes');
var CountryStore = require('../stores/CountryStore');
var GenderConstants = require('../constants/GenderConstants');
var NavLink = require('./NavLink');
var OuterView = require('./OuterView');
var ProgramTypes = require('../constants/ProgramTypes');

require('jquery-ui/effect-shake');

var RegistrationView = React.createClass({
  mixins: [
    React.addons.LinkedStateMixin,
    RRouter.RoutingContextMixin
  ],

  getInitialState: function() {
    return {
      errors: {},
      countries: [],
      first_name: null,
      last_name: null,
      username: null,
      password: null,
      password2: null,
      school_name: null,
      school_address: null,
      school_city: null,
      school_state: null,
      school_zip: null,
      school_country: "United States of America",
      school_international: false,
      program_type: ProgramTypes.CLUB,
      times_attended: null,
      beginner_delegates: null,
      intermediate_delegates: null,
      advanced_delegates: null,
      spanish_speaking_delegates: null,
      primary_name: null,
      primary_gender: GenderConstants.UNSPECFIED,
      primary_email: null,
      primary_phone: null,
      primary_type: ContactTypes.FACULTY,
      secondary_name: '',
      secondary_gender: GenderConstants.UNSPECFIED,
      secondary_email: '',
      secondary_phone: '',
      secondary_type: ContactTypes.FACULTY,
      country_pref1: 0,
      country_pref2: 0,
      country_pref3: 0,
      country_pref4: 0,
      country_pref5: 0,
      country_pref6: 0,
      country_pref7: 0,
      country_pref8: 0,
      country_pref9: 0,
      country_pref10: 0,
      prefers_bilingual: false,
      prefers_crisis: false,
      prefers_small_specialized: false,
      prefers_mid_large_specialized: false,
      registration_comments: '',
      loading: false,
      passwordValidating: false
    };
  },

  componentDidMount: function() {
    CountryStore.getCountries(function(countries) {
      this.setState({countries: countries});
    }.bind(this));
  },

  render: function() {
    var cx = React.addons.classSet;
    return (
      <OuterView>
        <form
          id="registration"
          className="registration-form"
          onSubmit={this._handleSubmit}>
          <div>
            <h1>Register for Berkeley Model United Nations</h1>
            <p>Please fill out the following information to register your school
            for BMUN 63. All fields are required except for Secondary Contact
            information.</p>
            <NavLink direction="left" href="/www/login">
              Back to Login
            </NavLink>
          </div>
          <div className="registration-fields">
            <hr />
            <h3>Account Information</h3>
            <input
              type="text"
              placeholder="First Name"
              valueLink={this.linkState('first_name')}
            />
            {this.renderError('first_name')}
            <input
              type="text"
              placeholder="Last Name"
              valueLink={this.linkState('last_name')}
            />
            {this.renderError('last_name')}
            <input
              type="text"
              placeholder="Username"
              valueLink={this.linkState('username')}
            />
            {this.renderError('username')}
            <input
              type="password"
              placeholder="Password"
              valueLink={this.linkState('password')}
              onBlur={this._handlePasswordBlur}
              onFocus={this._handlePasswordFocus}
            />
            {this.renderError('password')}
            <input
              type="password"
              placeholder="Password (confirm)"
              valueLink={this.linkState('password2')}
              onBlur={this._handlePasswordBlur}
              onFocus={this._handlePasswordFocus}
            />
            {this.renderPasswordConfirmError()}
            <hr />
            <h3>School Information</h3>
            <p className="instructions">Where is your school located?</p>
            <ul>
              <li>
                <label>
                  <input
                    type="radio"
                    value=''
                    onChange={this._handleInternationalChange}
                    checked={!this.state.school_international}
                  /> United States of America
                  </label>
              </li>
              <li>
                <label>
                  <input
                    type="radio"
                    value="international"
                    onChange={this._handleInternationalChange}
                    checked={this.state.school_international}
                  /> International
                </label>
              </li>
            </ul>
            <input
              type="text"
              placeholder="Official School Name"
              valueLink={this.linkState('school_name')}
            />
            {this.renderSchoolError('name')}
            <input
              type="text"
              placeholder="Street Address"
              valueLink={this.linkState('school_address')}
            />
            {this.renderSchoolError('address')}
            <input
              type="text"
              placeholder="City"
              valueLink={this.linkState('school_city')}
            />
            {this.renderSchoolError('city')}
            <input
              type="text"
              placeholder="State"
              valueLink={this.linkState('school_state')}
            />
            {this.renderSchoolError('state')}
            <input
              type="text"
              placeholder="Zip"
              valueLink={this.linkState('school_zip')}
            />
            {this.renderSchoolError('zip_code')}
            <input
              type="text"
              placeholder="Country"
              valueLink={this.state.school_international ? ''  :
                this.linkState('school_country')}
            />
            {this.renderSchoolError('country')}
            <hr />
            <h3>Program Information</h3>
            <p className="instructions">What category best describes your program?</p>
            <ul>
              <li>
                <label>
                  <input
                    type="radio"
                    checked={this.state.program_type == ProgramTypes.CLUB}
                    value={ProgramTypes.CLUB}
                    onChange={this._handleProgramTypeChange}
                  /> Club
                </label>
              </li>
              <li>
                <label>
                  <input
                    type="radio"
                    value={ProgramTypes.CLASS}
                    checked={this.state.program_type == ProgramTypes.CLASS}
                    onChange={this._handleProgramTypeChange}
                  /> Class
                </label>
              </li>
            </ul>
            <p className="instructions">Please tell us a bit more about your delegation this
              year.</p>
            <input
              type="text"
              placeholder="Number of BMUN sessions attended"
              valueLink={this.linkState("times_attended")}
            />
            {this.renderSchoolError('times_attended')}
            <input
              type="text"
              placeholder="Number of Beginner Delegates"
              valueLink={this.linkState('beginner_delegates')}
            />
            {this.renderSchoolError('beginner_delegates')}
            <input
              type="text"
              placeholder="Number of Intermediate Delegates"
              valueLink={this.linkState('intermediate_delegates')}
            />
            {this.renderSchoolError('intermediate_delegates')}
            <input
              type="text"
              placeholder="Number of Advanced Delegates"
              valueLink={this.linkState('advanced_delegates')}
            />
            {this.renderSchoolError('advanced_delegates')}
            <input
              type="text"
              placeholder="Number of Spanish Speaking Delegates"
              valueLink={this.linkState('spanish_speaking_delegates')}
            />
            {this.renderSchoolError('spanish_speaking_delegates')}
            <hr />
            <h3>Primary Contact</h3>
            {this.renderContactGenderField('primary_gender')}
            <input
              type="text"
              placeholder="Name"
              valueLink={this.linkState('primary_name')}
            />
            {this.renderSchoolError('primary_name')}
            <input
              type="text"
              placeholder="Email"
              valueLink={this.linkState('primary_email')}
            />
            {this.renderSchoolError('primary_email')}
            <input
              type="text"
              placeholder="Phone Number"
              valueLink={this.linkState('primary_phone')}
            />
            {this.renderSchoolError('primary_phone')}
            {this.renderContactTypeField('primary_type')}
            <hr />
            <h3>Secondary Contact</h3>
            {this.renderContactGenderField('secondary_gender')}
            <input
              type="text"
              placeholder="Name"
              valueLink={this.linkState('secondary_name')}
            />
            {this.renderSchoolError('secondary_name')}
            <input
              type="text"
              placeholder="Email"
              valueLink={this.linkState('secondary_email')}
            />
            {this.renderSchoolError('secondary_email')}
            <input
              type="text"
              placeholder="Phone Number"
              valueLink={this.linkState('secondary_phone')}
            />
            {this.renderSchoolError('secondary_phone')}
            {this.renderContactTypeField('secondary_type')}
            <hr />
            <h3>Country Preferences</h3>
            <p className="instructions">Please choose 10 United Nations Member States or
            Observers your school would like to represent. A reference list of
            countries and their relation to committees is available online.
            Please diversify your selection.</p>
            <ul>
              {this.renderCountryDropdown('01', 'country_pref1')}
              {this.renderCountryDropdown('02', 'country_pref2')}
              {this.renderCountryDropdown('03', 'country_pref3')}
              {this.renderCountryDropdown('04', 'country_pref4')}
              {this.renderCountryDropdown('05', 'country_pref5')}
              {this.renderCountryDropdown('06', 'country_pref6')}
              {this.renderCountryDropdown('07', 'country_pref7')}
              {this.renderCountryDropdown('08', 'country_pref8')}
              {this.renderCountryDropdown('09', 'country_pref9')}
              {this.renderCountryDropdown('10', 'country_pref10')}
            </ul>
            <hr />
            <h3>Special Committee Preferences</h3>
            <p className="instructions">Would your delegation be interested in being represented
            in the following small/specialized committees? Positions are limited
            and we may not be able to accomodate all preferences.</p>
            <ul>
              <li>
                <label>
                  <input
                    type="checkbox"
                    checked={this.state.prefers_bilingual}
                    onChange={this._handleBilingualChange}
                  />
                  Bilingual
                </label>
              </li>
              <li>
                <label>
                  <input
                    type="checkbox"
                    checked={this.state.prefers_crisis}
                    onChange={this._handleCrisisChange}
                  />
                  Crisis
                </label>
              </li>
              <li>
                <label>
                  <input
                    type="checkbox"
                    checked={this.state.prefers_small_specialized}
                    onChange={this._handleSmallSpecializedChange}
                  />
                  Small Specialized
                </label>
              </li>
              <li>
                <label>
                  <input
                    type="checkbox"
                    checked={this.state.prefers_mid_large_specialized}
                    onChange={this._handleMidLargeSpecializedChange}
                  />
                  Mid-large Specialized
                </label>
              </li>
            </ul>
            <hr />
            <h3>Comments</h3>
            <p className="instructions">If there are any further details you
            would like us to know about your participation in BMUN this year or
            general feedback about the registration process, please comment
            below.</p>
            <textarea
              cols="40"
              rows="7"
              valueLink={this.linkState('registration_comments')}
            />
            <hr />
              <NavLink direction="left" href="/www/login">
                Back to Login
              </NavLink>
              <div className="right">
                <span className="help-text"><em>All done?</em></span>
                <Button
                  color="green"
                  loading={this.state.loading}
                  type="submit">
                  Register
                </Button>
              </div>
          </div>
        </form>
      </OuterView>
    );
  },

  renderCommitteeOptions: function() {
    return this.state.countries.map(function(country) {
      return <option key={country.id} value={country.id}>{country.name}</option>
    });
  },

  renderCountryDropdown: function(labelNum, fieldName) {
    return (
      <li>
        <label>{labelNum}</label>
        <select
          onChange={this._handleCountryChange.bind(this, fieldName)}
          value={this.state[fieldName]}>
          <option value="0">No Preference</option>
          {this.renderCommitteeOptions()}
        </select>
      </li>
    );
  },

  renderContactGenderField: function(name) {
    return (
      <div className="contact-select">
        <select valueLink={this.linkState(name)}>
          <option
            key={GenderConstants.UNSPECFIED}
            value={GenderConstants.UNSPECFIED}>
            Unspecified
          </option>
          <option
            key={GenderConstants.MALE}
            value={GenderConstants.MALE}>
            Mr.
          </option>
          <option
            key={GenderConstants.FEMALE}
            value={GenderConstants.FEMALE}>
            Mrs./Ms.
          </option>
          <option
            key={GenderConstants.OTHER}
            value={GenderConstants.OTHER}>
            Other
          </option>
        </select>
      </div>
    );
  },

  renderContactTypeField: function(name) {
    return (
      <div className="contact-select">
        <select valueLink={this.linkState(name)}>
          <option
            key={ContactTypes.STUDENT}
            value={ContactTypes.STUDENT}>
            Student
          </option>
          <option
            key={ContactTypes.FACULTY}
            value={ContactTypes.FACULTY}>
            Faculty
          </option>
        </select>
      </div>
    );
  },

  renderError: function(field) {
    if (this.state.errors[field]) {
      return (
        <div>
          <label className="error">
            {this.state.errors[field]}
          </label>
        </div>
      );
    }

    return null;
  },

  renderPasswordConfirmError: function() {
    if (this.state.passwordValidating &&
        this.state.password !== this.state.password2) {
      return (
        <div>
          <label className="error">Please enter the same password again.</label>
        </div>
      );
    }
    return null;
  },

  renderSchoolError: function(field) {
    if (this.state.errors.school &&
        this.state.errors.school[0][field]) {
      return (
        <div>
          <label className="error">
            {this.state.errors.school[0][field]}
          </label>
        </div>
      );
    }

    return null;
  },

  _handlePasswordBlur: function() {
    this.setState({passwordValidating: true});
  },

  _handlePasswordFocus: function() {
    this.setState({passwordValidating: false});
  },

  _handleProgramTypeChange: function(event) {
    this.setState({program_type: event.target.value});
  },

  _handleCountryChange: function(fieldName, event) {
    var change = {};
    change[fieldName] = event.target.value;
    this.setState(change);
  },

  _handleInternationalChange: function(event) {
    this.setState({school_international: !!event.target.value});
  },

  _handleBilingualChange: function(event) {
    this.setState({prefers_bilingual: !this.state.prefers_bilingual});
  },

  _handleCrisisChange: function(event) {
    this.setState({prefers_crisis: !this.state.prefers_crisis});
  },

  _handleSmallSpecializedChange: function(event) {
    this.setState({prefers_small_specialized:
      !this.state.prefers_small_specialized});
  },

  _handleMidLargeSpecializedChange: function(event) {
    this.setState({prefers_mid_large_specialized:
      !this.state.prefers_mid_large_specialized});
  },

  _handleSubmit: function(event) {
    this.setState({loading: true});
    $.ajax({
      type: 'POST',
      url: '/api/users',
      data: JSON.stringify({
        first_name: this.state.first_name,
        last_name: this.state.last_name,
        username: this.state.username,
        password: this.state.password,
        password2: this.state.password2,
        school: {
          name: this.state.school_name,
          address: this.state.school_address,
          city: this.state.school_city,
          state: this.state.school_state,
          zip_code: this.state.school_zip,
          country: this.state.school_country,
          international: this.state.school_international,
          program_type: this.state.program_type,
          times_attended: this.state.times_attended,
          beginner_delegates: this.state.beginner_delegates,
          intermediate_delegates: this.state.intermediate_delegates,
          advanced_delegates: this.state.advanced_delegates,
          spanish_speaking_delegates: this.state.spanish_speaking_delegates,
          primary_name: this.state.primary_name,
          primary_gender: this.state.primary_gender,
          primary_email: this.state.primary_email,
          primary_phone: this.state.primary_phone,
          primary_type: this.state.primary_type,
          secondary_name: this.state.secondary_name,
          secondary_gender: this.state.secondary_gender,
          secondary_email: this.state.secondary_email,
          secondary_phone: this.state.secondary_phone,
          secondary_type: this.state.secondary_type,
          countrypreferences: [
            this.state.country_pref1,
            this.state.country_pref2,
            this.state.country_pref3,
            this.state.country_pref4,
            this.state.country_pref5,
            this.state.country_pref6,
            this.state.country_pref7,
            this.state.country_pref8,
            this.state.country_pref9,
            this.state.country_pref10
          ],
          prefers_bilingual: this.state.prefers_bilingual,
          prefers_crisis: this.state.prefers_crisis,
          prefers_small_specialized: this.state.prefers_small_specialized,
          prefers_mid_large_specialized:
            this.state.prefers_mid_large_specialized,
          registration_comments: this.state.registration_comments
        }
      }),
      success: this._handleSuccess,
      error: this._handleError,
      contentType: 'application/json'
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    this.navigate('/www/register/success');
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
      $(this.getDOMNode()).effect(
        'shake',
        {direction: 'up', times: 2, distance: 2},
        250
      );
    }.bind(this));
  }
});

module.exports = RegistrationView;
