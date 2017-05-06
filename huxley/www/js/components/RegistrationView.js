/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var cx = require('classnames');
var React = require('react');
var ReactRouter = require('react-router');

var Button = require('components/Button');
var CommitteeStore = require('stores/CommitteeStore');
var ContactTypes = require('constants/ContactTypes');
var ConferenceContext = require('components/ConferenceContext');
var CountrySelect = require('components/CountrySelect');
var CountryStore = require('stores/CountryStore');
var GenderConstants = require('constants/GenderConstants');
var NavLink = require('components/NavLink');
var NumberInput = require('components/NumberInput');
var OuterView = require('components/OuterView');
var PhoneInput = require('components/PhoneInput');
var ProgramTypes = require('constants/ProgramTypes');
var StatusLabel = require('components/StatusLabel');
var TextInput = require('components/TextInput');
var _handleChange = require('utils/_handleChange');

require('css/RegistrationView.less');
require('jquery-ui/effect-shake');

var USA = 'United States of America';

var RegistrationView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  getInitialState: function() {
    return {
      errors: {},
      countries: Object.values(CountryStore.getCountries()),
      committees: Object.values(CommitteeStore.getSpecialCommittees()),
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
      chinese_speaking_delegates: '',
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
      committee_prefs: [],
      registration_comments: '',
      loading: false,
      passwordValidating: false
    };
  },

  componentDidMount: function() {
    this._committeesToken = CommitteeStore.addListener(() => {
      this.setState({
        committees: Object.values(CommitteeStore.getSpecialCommittees())
      });
    });

    this._countriesToken = CountryStore.addListener(() => {
      this.setState({countries: Object.values(CountryStore.getCountries())});
    });
  },

  componentWillUnmount: function() {
    this._committeesToken && this._committeesToken.remove();
    this._countriesToken && this._countriesToken.remove();
  },

  render: function() {
    var conference = this.context.conference;
    return (
      <OuterView>
        <form id="registration" onSubmit={this._handleSubmit}>
          <div>
            <h1>Register for Berkeley Model United Nations</h1>
            <p>Please fill out the following information to register your school
            for BMUN {conference.session}. All fields are required except for Secondary Contact
            information. Please note that BMUN is a high school level conference.</p>
            <NavLink direction="left" href="/login">
              Back to Login
            </NavLink>
          </div>
          <div>
            <hr />
            <h3>Account Information</h3>
            <RegistrationTextInput
              errors={this.state.errors['first_name']}
              placeholder="First Name"
              onChange={_handleChange.bind(this, 'first_name')}
              value={this.state.first_name}
            />
            <RegistrationTextInput
              errors={this.state.errors['last_name']}
              placeholder="Last Name"
              onChange={_handleChange.bind(this, 'last_name')}
              value={this.state.last_name}
            />
            <RegistrationTextInput
              errors={this.state.errors['username']}
              placeholder="Username"
              onChange={_handleChange.bind(this, 'username')}
              value={this.state.username}
            />
            <RegistrationTextInput
              errors={this.state.errors['password']}
              type="password"
              placeholder="Password"
              value={this.state.password}
              onChange={this._handlePasswordChange}
              onBlur={this._handlePasswordBlur}
              onFocus={this._handlePasswordFocus}
            />
            <RegistrationTextInput
              errors={this._getPasswordConfirmError()}
              type="password"
              placeholder="Password (confirm)"
              value={this.state.password2}
              onChange={this._handlePasswordConfirmChange}
              onBlur={this._handlePasswordBlur}
              onFocus={this._handlePasswordFocus}
            />
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
            <RegistrationTextInput
              errors={this._getSchoolErrors('name')}
              placeholder="Official School Name"
              onChange={_handleChange.bind(this, 'school_name')}
              value={this.state.school_name}
            />
            <RegistrationTextInput
              errors={this._getSchoolErrors('address')}
              placeholder="Street Address"
              value={this.state.school_address}
              onChange={_handleChange.bind(this, 'school_address')}
            />
            <RegistrationTextInput
              errors={this._getSchoolErrors('city')}
              placeholder="City"
              onChange={_handleChange.bind(this, 'school_city')}
              value={this.state.school_city}
            />
            <RegistrationTextInput
              errors={this._getSchoolErrors('state')}
              placeholder="State"
              onChange={_handleChange.bind(this, 'school_state')}
              value={this.state.school_state}
            />
            <RegistrationTextInput
              errors={this._getSchoolErrors('zip_code')}
              placeholder="Zip"
              onChange={_handleChange.bind(this, 'school_zip')}
              value={this.state.school_zip}
            />
            <RegistrationTextInput
              errors={this._getSchoolErrors('country')}
              placeholder="Country"
              value={this._getSchoolCountry()}
              onChange={_handleChange.bind(this, 'school_country')}
              disabled={!this.state.school_international}
              isControlled={true}
            />
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
            <NumberInput
              placeholder="Number of BMUN sessions attended"
              onChange={_handleChange.bind(this, 'times_attended')}
              value={this.state.times_attended}
            />
            {this.renderSchoolError('times_attended')}
            <NumberInput
              placeholder="Tentative Number of Beginner Delegates"
              onChange={_handleChange.bind(this, 'beginner_delegates')}
              value={this.state.beginner_delegates}
            />
            <label className="hint">
              Beginner: Attended 0-3 conferences, not very familiar with Model
              United Nations.
            </label>
            {this.renderSchoolError('beginner_delegates')}
            <NumberInput
              placeholder="Tentative Number of Intermediate Delegates"
              onChange={_handleChange.bind(this, 'intermediate_delegates')}
              value={this.state.intermediate_delegates}
            />
            <label className="hint">
              Intermediate: Attended 4-7 conferences, little to no practice in
              advanced committees.
            </label>
            {this.renderSchoolError('intermediate_delegates')}
            <NumberInput
              placeholder="Tentative Number of Advanced Delegates"
              onChange={_handleChange.bind(this, 'advanced_delegates')}
              value={this.state.advanced_delegates}
            />
            <label className="hint">
              Advanced: Attended more than seven conferences, has participated
              in many diverse committees.
            </label>
            {this.renderSchoolError('advanced_delegates')}
            <p className="instructions">Tentative Total Number of Delegates: {this._handleDelegateSum()}</p>
            <hr />
            <h3>Primary Contact</h3>
            {this.renderContactGenderField('primary_gender')}
            <RegistrationTextInput
              errors={this._getSchoolErrors('primary_name')}
              placeholder="Name"
              onChange={_handleChange.bind(this, 'primary_name')}
              value={this.state.primary_name}
            />
            <RegistrationTextInput
              errors={this._getSchoolErrors('primary_email')}
              placeholder="Email"
              onChange={_handleChange.bind(this, 'primary_email')}
              value={this.state.primary_email}
            />
            <RegistrationPhoneInput
              errors={this._getSchoolErrors('primary_phone')}
              onChange={this._handlePrimaryPhoneChange}
              value={this.state.primary_phone}
              isInternational={this.state.school_international}
            />
            {this.renderContactTypeField('primary_type')}
            <hr />
            <h3>Secondary Contact</h3>
            {this.renderContactGenderField('secondary_gender')}
            <RegistrationTextInput
              errors={this._getSchoolErrors('secondary_name')}
              placeholder="Name"
              onChange={_handleChange.bind(this, 'secondary_name')}
              value={this.state.secondary_name}
            />
            <RegistrationTextInput
              errors={this._getSchoolErrors('secondary_email')}
              placeholder="Email"
              onChange={_handleChange.bind(this, 'secondary_email')}
              value={this.state.secondary_email}
            />
            <RegistrationPhoneInput
              errors={this._getSchoolErrors('secondary_phone')}
              onChange={this._handleSecondaryPhoneChange}
              value={this.state.secondary_phone}
              isInternational={this.state.school_international}
            />
            {this.renderContactTypeField('secondary_type')}
            <hr />
            <h3>Country Preferences</h3>
            <p className="instructions">Please choose 10 United Nations Member States or
            Observers your school would like to represent. A reference list of
            countries and their relation to committees is
            available <a href="http://www.un.org/en/member-states/" target="_blank">online</a>.
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
            Positions are limited and we may not be able to accommodate all
            preferences. You can find a reference to our
            committees <a href="http://www.bmun.org/committees" target="_blank">
            here</a>.</p>
            <ul>
              {this.renderCommittees()}
            </ul>
            <NumberInput
              placeholder="Number of Spanish Speaking Delegates"
              onChange={_handleChange.bind(this, 'spanish_speaking_delegates')}
              value={this.state.spanish_speaking_delegates}
            />
            {this.renderSchoolError('spanish_speaking_delegates')}
            <NumberInput
              placeholder="Number of Chinese Speaking Delegates"
              onChange={_handleChange.bind(this, 'chinese_speaking_delegates')}
              value={this.state.chinese_speaking_delegates}
            />
            {this.renderSchoolError('chinese_speaking_delegates')}
            <hr />
            <h3>Comments</h3>
            <p className="instructions">If there are any further details you
            would like us to know about your participation in BMUN this year or
            general feedback about the registration process, please comment
            below.</p>
            <textarea
              className="text-input"
              cols="40"
              rows="7"
              onChange={_handleChange.bind(this, 'registration_comments')}
              value={this.state.registration_comments}
            />
            <hr />
              <NavLink direction="left" href="/login">
                Back to Login
              </NavLink>
              <div style={{float: 'right'}}>
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
          onChange={_handleChange.bind(this, fieldName)}
          countries={this.state.countries}
          selectedCountryID={this.state[fieldName]}
          countryPreferences={[
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
          ]}
        />
      </li>
    );
  },

  renderCommittees: function() {
    return this.state.committees.map(function(committee) {
      return (
        <li>
          <label name="committee_prefs">
            <input
              className="choice"
              type="checkbox"
              name="committee_prefs"
              onChange={this._handleCommitteePreferenceChange.bind(this, committee)}
            />
            {committee.full_name}
          </label>
        </li>
      );
    }, this);
  },

  renderContactGenderField: function(name) {
    return (
      <select
        className="contact-select reg-field"
        onChange={_handleChange.bind(this, name)}
        value={this.state[name]}>
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
    );
  },

  renderContactTypeField: function(name) {
    return (
      <select
        className="contact-select reg-field"
        onChange={_handleChange.bind(this, name)}
        value={this.state[name]}>
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
    );
  },

  renderError: function(field) {
    if (this.state.errors[field]) {
      return (
        <StatusLabel status="error">
          {this.state.errors[field]}
        </StatusLabel>
      );
    }

    return null;
  },

  _getPasswordConfirmError() {
    if (this.state.passwordValidating &&
        this.state.password !== this.state.password2) {
      return 'Please enter the same password again.';
    }
  },

  renderSchoolError: function(field) {
    if (this.state.errors.school &&
        this.state.errors.school[field]) {
      return (
        <StatusLabel status="error">
          {this.state.errors.school[field]}
        </StatusLabel>
      );
    }

    return null;
  },

  _getSchoolErrors(field) {
    if (this.state.errors.school) {
      return this.state.errors.school[field];
    }
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

  _handlePasswordBlur: function() {
    this.setState({passwordValidating: true});
  },

  _handlePasswordFocus: function() {
    this.setState({passwordValidating: false});
  },

  _handleProgramTypeChange: function(event) {
    this.setState({program_type: event.target.value});
  },

  _handleCommitteePreferenceChange: function(committee) {
    var index = this.state.committee_prefs.indexOf(committee.id);
    if (index < 0) {
      this.setState({
        committee_prefs: this.state.committee_prefs.concat(committee.id),
      });
    } else {
      this.setState({
        committee_prefs: this.state.committee_prefs.filter(function(id) {
          return committee.id !== id;
        }),
      });
    }
  },

  _handleInternationalChange: function(event) {
    this.setState({school_international: !!event.target.value});
  },

  _handlePrimaryPhoneChange: function(number) {
    this.setState({primary_phone: number});
  },

  _handleSecondaryPhoneChange: function(number) {
    this.setState({secondary_phone: number});
  },

  _handlePasswordChange: function(password) {
    this.setState({password});
  },

  _handlePasswordConfirmChange: function(password2) {
    this.setState({password2});
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
          chinese_speaking_delegates: this.state.chinese_speaking_delegates,
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
          committeepreferences: this.state.committee_prefs,
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
      this.history.pushState(null, '/register/waitlist');
    } else {
      this.history.pushState(null, '/register/success');
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

const RegistrationTextInput = React.createClass({
  propTypes: {
    errors: React.PropTypes.arrayOf(React.PropTypes.string),
    onChange: React.PropTypes.func,
    placeholder: React.PropTypes.string,
    value: React.PropTypes.string,
    type: React.PropTypes.oneOf(['text', 'password']),
  },

  render() {
    const {errors, ...inputProps} = this.props;
    return (
      <div className="reg-field">
        <TextInput {...inputProps} />
        {errors && errors.map(error =>
          <StatusLabel status="error">{error}</StatusLabel>
        )}
      </div>
    );
  },
});

const RegistrationPhoneInput = React.createClass({
  propTypes: {
    errors: React.PropTypes.arrayOf(React.PropTypes.string),
    onChange: React.PropTypes.func,
    placeholder: React.PropTypes.string,
    value: React.PropTypes.string,
  },

  render() {
    const {errors, ...inputProps} = this.props;
    return (
      <div className="reg-field">
        <PhoneInput {...inputProps} />
        {errors && errors.map(error =>
          <StatusLabel status="error">{error}</StatusLabel>
        )}
      </div>
    );
  },
});

module.exports = RegistrationView;
