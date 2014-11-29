/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var console = require('console');

var $ = require('jquery');
var React = require('react/addons');
var Router = require('react-router');

var Button = require('./Button');
var ContactTypes = require('../constants/ContactTypes');
var CountrySelect = require('./CountrySelect');
var CountryStore = require('../stores/CountryStore');
var GenderConstants = require('../constants/GenderConstants');
var NavLink = require('./NavLink');
var NumberInput = require('./NumberInput');
var OuterView = require('./OuterView');
var PhoneInput = require('./PhoneInput');
var ProgramTypes = require('../constants/ProgramTypes');

require('jquery-ui/effect-shake');

var USA = 'United States of America';

var RegistrationView = React.createClass({
  mixins: [
    React.addons.LinkedStateMixin,
    Router.Navigation,
  ],

  getInitialState: function() {
    return {
      errors: {},
      countries: [],
      first_name: '',
      last_name: '',
      username: '',
      password: null,
      password2: null,
      school_name: '',
      school_address: '',
      school_city: '',
      school_state: '',
      school_zip: '',
      school_country: '',
      school_international: false,
      program_type: ProgramTypes.CLUB,
      times_attended: '',
      beginner_delegates: '',
      intermediate_delegates: '',
      advanced_delegates: '',
      spanish_speaking_delegates: '',
      primary_name: '',
      primary_gender: GenderConstants.UNSPECFIED,
      primary_email: '',
      primary_phone: '',
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
      prefers_specialized_regional: false,
      prefers_crisis: false,
      prefers_alternative: false,
      prefers_press_corps: false,
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
            <NavLink direction="left" href="/login">
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
              value={this._getSchoolCountry()}
              onChange={this._handleSchoolCountryChange}
              disabled={!this.state.school_international}
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
              year. Provide us with the tentative number of beginner,
              intermediate, and advanced delegates you intend to bring to BMUN.
              Try to provide us with realistic estimates for your delegate
              numbers in each category so we can provide your delegation with
              the appropriate number and type of assignments.</p>
            <input
              type="text"
              placeholder="Number of BMUN sessions attended"
              valueLink={this.linkState("times_attended")}
            />
            {this.renderSchoolError('times_attended')}
            <NumberInput
              placeholder="Tentative Number of Beginner Delegates"
              onChange={this._handleNumDelChange.bind(this, 'beginner_delegates')}
              value={this.state.beginner_delegates}
            />
            <label className="hint">
              Beginner: Attended 0-3 conferences, not very familiar with Model
              United Nations.
            </label>
            {this.renderSchoolError('beginner_delegates')}
            <NumberInput
              placeholder="Tentative Number of Intermediate Delegates"
              onChange={this._handleNumDelChange.bind(this, 'intermediate_delegates')}
              value={this.state.intermediate_delegates}
            />
            <label className="hint">
              Intermediate: Attended 4-7 conferences, little to no practice in
              advanced committees.
            </label>
            {this.renderSchoolError('intermediate_delegates')}
            <NumberInput
              placeholder="Tentative Number of Advanced Delegates"
              onChange={this._handleNumDelChange.bind(this, 'advanced_delegates')}
              value={this.state.advanced_delegates}
            />
            <label className="hint">
              Advanced: Attended more than seven conferences, has participated
              in many diverse committees.
            </label>
            {this.renderSchoolError('advanced_delegates')}
            <p>Tentative Total Number of Delegates: {this._handleDelegateSum()}</p>
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
            <PhoneInput
              onChange={this._handlePrimaryPhoneChange}
              value={this.state.primary_phone}
              isInternational={this.state.school_international}
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
            <PhoneInput
              onChange={this._handleSecondaryPhoneChange}
              value={this.state.secondary_phone}
              isInternational={this.state.school_international}
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
            <p className="instructions">Would your delegation be interested in
            being represented in the following small/specialized committees?
            Positions are limited and we may not be able to accomodate all
            preferences. You can find a reference to our
            committees <a href="http://bmun.org/Committees.php" target="_blank">
            here</a>.</p>
            <ul>
              <li>
                <label>
                  <input
                    type="checkbox"
                    checked={this.state.prefers_bilingual}
                    onChange={this._handleBilingualChange}
                  />
                  Bilingual - (IDB)
                </label>
              </li>
              <li>
                <label>
                  <input
                    type="checkbox"
                    checked={this.state.prefers_specialized_regional}
                    onChange={this._handleSpecializedRegionalChange}
                  />
                  Specialized/Regional - (SC, G20, EU, APEC)
                </label>
              </li>
              <li>
                <label>
                  <input
                    type="checkbox"
                    checked={this.state.prefers_crisis}
                    onChange={this._handleCrisisChange}
                  />
                  Crisis - (IFC, KHAN, ACC, JCC)
                </label>
              </li>
              <li>
                <label>
                  <input
                    type="checkbox"
                    checked={this.state.prefers_alternative}
                    onChange={this._handleAlternativeChange}
                  />
                  Alternative - (ICC, UNGC)
                </label>
              </li>
              <li>
                <label>
                  <input
                    type="checkbox"
                    checked={this.state.prefers_press_corps}
                    onChange={this._handlePressCorpsChange}
                  />
                  Press Corps
                </label>
              </li>
              <li>
                <input
                  type="text"
                  placeholder="Number of Spanish Speaking Delegates"
                  valueLink={this.linkState('spanish_speaking_delegates')}
                />
                {this.renderSchoolError('spanish_speaking_delegates')}
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
              <NavLink direction="left" href="/login">
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

  renderCountryDropdown: function(labelNum, fieldName) {
    return (
      <li>
        <label>{labelNum}</label>
        <CountrySelect
          onChange={this._handleCountryPrefChange.bind(this, fieldName)}
          countries={this.state.countries}
          selectedCountryID={this.state[fieldName]}
        />
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
        <label className="hint error">
          {this.state.errors[field]}
        </label>
      );
    }

    return null;
  },

  renderPasswordConfirmError: function() {
    if (this.state.passwordValidating &&
        this.state.password !== this.state.password2) {
      return (
        <label className="hint error">
          Please enter the same password again.
        </label>
      );
    }

    return null;
  },

  renderSchoolError: function(field) {
    if (this.state.errors.school &&
        this.state.errors.school[0][field]) {
      return (
        <label className="hint error">
          {this.state.errors.school[0][field]}
        </label>
      );
    }

    return null;
  },

  _handleDelegateSum: function() {
    var sum = 0;
    if (this.state.beginner_delegates) {
      sum += parseInt(this.state.beginner_delegates, 10) || 0;
    } if (this.state.intermediate_delegates) {
      sum += parseInt(this.state.intermediate_delegates, 10) || 0;
    } if (this.state.advanced_delegates) {
      sum += parseInt(this.state.advanced_delegates, 10) || 0;
    }
    return sum;
  },

  _handleNumDelChange: function(fieldName, value) {
    var change = {};
    change[fieldName] = value;
    this.setState(change);
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

  _handleCountryPrefChange: function(fieldName, event) {
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

  _handleSpecializedRegionalChange: function(event) {
    this.setState({
      prefers_specialized_regional: !this.state.prefers_specialized_regional
    });
  },

  _handleCrisisChange: function(event) {
    this.setState({prefers_crisis: !this.state.prefers_crisis});
  },

  _handleAlternativeChange: function(event) {
    this.setState({prefers_alternative: !this.state.prefers_alternative});
  },

  _handlePressCorpsChange: function(event) {
    this.setState({prefers_press_corps: !this.state.prefers_press_corps});
  },

  _handlePrimaryPhoneChange: function(number) {
    this.setState({
      primary_phone: number
    });
  },

  _handleSecondaryPhoneChange: function(number) {
    this.setState({
      secondary_phone: number
    });
  },

  _handleSchoolCountryChange: function(event) {
    this.setState({school_country: event.target.value});
  },

  _getSchoolCountry: function() {
    return this.state.school_international ? this.state.school_country : USA;
  },

  _handleSubmit: function(event) {
    this.setState({loading: true});
    $.ajax({
      type: 'POST',
      url: '/api/users',
      data: JSON.stringify({
        first_name: this.state.first_name.trim(),
        last_name: this.state.last_name.trim(),
        username: this.state.username.trim(),
        email: this.state.primary_email.trim(),
        password: this.state.password,
        password2: this.state.password2,
        school: {
          name: this.state.school_name.trim(),
          address: this.state.school_address.trim(),
          city: this.state.school_city.trim(),
          state: this.state.school_state.trim(),
          zip_code: this.state.school_zip.trim(),
          country: this._getSchoolCountry().trim(),
          international: this.state.school_international,
          program_type: this.state.program_type,
          times_attended: this.state.times_attended.trim(),
          beginner_delegates: this.state.beginner_delegates,
          intermediate_delegates: this.state.intermediate_delegates,
          advanced_delegates: this.state.advanced_delegates,
          spanish_speaking_delegates: this.state.spanish_speaking_delegates,
          primary_name: this.state.primary_name.trim(),
          primary_gender: this.state.primary_gender,
          primary_email: this.state.primary_email.trim(),
          primary_phone: this.state.primary_phone.trim(),
          primary_type: this.state.primary_type,
          secondary_name: this.state.secondary_name.trim(),
          secondary_gender: this.state.secondary_gender,
          secondary_email: this.state.secondary_email.trim(),
          secondary_phone: this.state.secondary_phone.trim(),
          secondary_type: this.state.secondary_type,
          country_preferences: [
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
          prefers_specialized_regional: this.state.prefers_specialized_regional,
          prefers_crisis: this.state.prefers_crisis,
          prefers_alternative: this.state.prefers_alternative,
          prefers_press_corps: this.state.prefers_press_corps,
          registration_comments: this.state.registration_comments.trim()
        }
      }),
      success: this._handleSuccess,
      error: this._handleError,
      contentType: 'application/json'
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    if (data.school.waitlist) {
      this.transitionTo('/register/waitlist');
    } else {
      this.transitionTo('/register/success');
    }
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
        {direction: 'up', times: 2, distance: 2},
        250
      );
    }.bind(this));
  }
});

module.exports = RegistrationView;
