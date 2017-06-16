/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

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
var ServerAPI = require('lib/ServerAPI');
var StatusLabel = require('components/StatusLabel');
var TextInput = require('components/TextInput');
var TextTemplate = require('components/TextTemplate');
var _handleChange = require('utils/_handleChange');

require('css/RegistrationView.less');
var RegistrationViewText = require('text/RegistrationViewText.md');

var USA = 'United States of America';

var _accessSafe = function(obj, key) {
  return obj && obj[key];
};

var RegistrationView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
    shake: React.PropTypes.func,
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

    //I feel like this (And a lot of others in this section) could 
    //Be reduced with some kind of mapping,
    //But there's no obvious way to map over Objects in JS so :/
    var accountInformationErrors = {
      'first_name': this.state.errors['first_name'], 
      'last_name': this.state.errors['last_name'], 
      'username': this.state.errors['username'], 
      'password': this.state.errors['password'],
      'password_confirm': this._getPasswordConfirmError(),
    };
    var accountInformationHandlers = {
      'first_name': _handleChange.bind(this,'first_name'),
      'last_name': _handleChange.bind(this,'last_name'),
      'username': _handleChange.bind(this,'username'),
      'password': this._handlePasswordChange,
      'password_confirm': this.handlePasswordConfirmChange,
    };
    var accountInformationValues = {
      'first_name': this.state.first_name,
      'last_name': this.state.last_name,
      'username': this.state.username,
      'password': this.state.password,
      'password_confirm': this.state.password2,
    };

    var schoolInformationErrors = {
      'school_name': this._getSchoolErrors('name'),
      'school_address': this._getSchoolErrors('address'),
      'school_city': this._getSchoolErrors('city'),
      'school_state': this._getSchoolErrors('state'),
      'school_zip': this._getSchoolErrors('zip_code'),
      'school_country': this._getSchoolErrors('country'),
    };
    var schoolInformationHandlers = {
      'school_name': _handleChange.bind(this,'school_name'),
      'school_address': _handleChange.bind(this,'school_address'),
      'school_city': _handleChange.bind(this,'school_city'),
      'school_state': _handleChange.bind(this,'school_state'),
      'school_zip': _handleChange.bind(this,'school_zip'),
      'school_country': _handleChange.bind(this,'school_country'),
    };
    var schoolInformationValues = {
      'school_name': this.state.school_name,
      'school_address': this.state.school_address,
      'school_city': this.state.school_city,
      'school_state': this.state.school_state,
      'school_zip': this.state.school_zip,
      'school_country': this._getSchoolCountry(),
    };
    
    var programInformationHandlers = {
      'times_attended': _handleChange.bind(this, 'times_attended'),
      'beginner_delegates': _handleChange.bind(this, 'beginner_delegates'),
      'intermediate_delegates': _handleChange.bind(this, 'intermediate_delegates'),
      'advanced_delegates': _handleChange.bind(this, 'advanced_delegates'),
    };
    var programInformationValues = {
      'times_attended': this.state.times_attended,
      'beginner_delegates': this.state.beginner_delegates,
      'intermediate_delegates': this.state.intermediate_delegates,
      'advanced_delegates': this.state.advanced_delegates,
    };
    var programInformationErrors = {
      'times_attended': this.renderSchoolError('times_attended'),
      'beginner_delegates': this.renderSchoolError('beginner_delegates'),
      'intermediate_delegates': this.renderSchoolError('intermediate_delegates'),
      'advanced_delegates': this.renderSchoolError('advanced_delegates'),
    };

    var primaryContactHandlers = {
      'primary_name': _handleChange.bind(this, 'primary_name'),
      'primary_email': _handleChange.bind(this, 'primary_email'),
      'primary_phone': this._handlePrimaryPhoneChange,
    };
    var primaryContactValues = {
      'primary_name': this.state.primary_name,
      'primary_email': this.state.primary_email,
      'primary_phone': this.state.primary_phone,
    };
    var primaryContactErrors = {
      'primary_name': this._getSchoolErrors('primary_name'),
      'primary_email': this._getSchoolErrors('primary_email'),
      'primary_phone': this._getSchoolErrors('primary_phone'),
    };

    var secondaryContactHandlers = {
      'secondary_name': _handleChange.bind(this, 'secondary_name'),
      'secondary_email': _handleChange.bind(this, 'secondary_email'),
      'secondary_phone': this._handleSecondaryPhoneChange,
    };
    var secondaryContactValues = {
      'secondary_name': this.state.secondary_name,
      'secondary_email': this.state.secondary_email,
      'secondary_phone': this.state.secondary_phone,
    };
    var secondaryContactErrors = {
      'secondary_name': this._getSchoolErrors('secondary_name'),
      'secondary_email': this._getSchoolErrors('secondary_email'),
      'secondary_phone': this._getSchoolErrors('secondary_phone'),
    };

    var specialCommitteeHandlers = {
      'spanish_speaking_delegates': _handleChange.bind(this, 'spanish_speaking_delegates'),
      'chinese_speaking_delegates': _handleChange.bind(this, 'chinese_speaking_delegates'),
    };
    var specialCommitteeValues = {
      'spanish_speaking_delegates': this.state.spanish_speaking_delegates,
      'chinese_speaking_delegates': this.state.chinese_speaking_delegates,
    };
    var specialCommitteeErrors = {
      'spanish_speaking_delegates': this.renderSchoolError('spanish_speaking_delegates'),
      'chinese_speaking_delegates': this.renderSchoolError('chinese_speaking_delegates'),
    };

    return (
      <OuterView>
        <form id="registration" onSubmit={this._handleSubmit}>
          <RegistrationHeader session={conference.session} />
          <hr />
          <AccountInformation 
            handlers={accountInformationHandlers} 
            errors={accountInformationErrors} 
            accountInformation={accountInformationValues} 
            blur={this._handlePasswordBlur} 
            focus={this._handlePasswordFocus}
          />
          <hr />
          <SchoolInformation  
            handlers={schoolInformationHandlers} 
            errors={schoolInformationErrors} 
            schoolInformation={schoolInformationValues} 
            handleInternationalChange={this._handleInternationalChange} 
            schoolInternational={this.state.school_international} 
          />
          <hr />
          <ProgramInformation 
            handlers={programInformationHandlers} 
            errors={programInformationErrors} 
            programInformation={programInformationValues} 
            handleProgramTypeChange={this._handleProgramTypeChange}
            programType={this.state.program_type}
          />
          <hr />
          <PrimaryContact 
            handlers={primaryContactHandlers} 
            primaryContactInformation={primaryContactValues} 
            errors={primaryContactErrors} 
            renderContactGenderField={this.renderContactGenderField} 
            renderContactTypeField={this.renderContactTypeField} 
            isInternational={this.state.school_international} 
          />
          <hr />
          <SecondaryContact 
            handlers={secondaryContactHandlers} 
            secondaryContactInformation={secondaryContactValues} 
            errors={secondaryContactErrors} 
            renderContactGenderField={this.renderContactGenderField} 
            renderContactTypeField={this.renderContactTypeField} 
            isInternational={this.state.school_international}
          />
          <hr />
            <CountryPreferences
              renderCountryDropdown={this.renderCountryDropdown}
            />
          <hr />
            <SpecialCommitteePreferences 
              handlers={specialCommitteeHandlers} 
              errors={specialCommitteeErrors}
              specialCommitteePrefValues={specialCommitteeValues} 
              renderCommittees={this.renderCommittees}
            />
          <hr />
            <Comments
              handler={_handleChange.bind(this, 'registration_comments')} 
              value={this.state.registration_comments} 
            />
          <hr />
            <RegistrationFooter 
              loading={this.state.loading} 
            />
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
    ServerAPI.register({
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
      },
    }).then(this._handleSuccess, this._handleError);
    event.preventDefault();
  },

  _handleSuccess: function(response) {
    if (response.school.waitlist) {
      this.history.pushState(null, '/register/waitlist');
    } else {
      this.history.pushState(null, '/register/success');
    }
  },

  _handleError: function(response) {
    if (!response) {
      return;
    }

    this.setState({
      errors: response,
      loading: false
    }, () => {
      this.context.shake && this.context.shake();
    });
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

const RegistrationHeader = React.createClass({
  propTypes: {
    session: React.PropTypes.number,
  },

  render: function() {
    return (
      <div>
        <TextTemplate conferenceSession={this.props.session}>
          {RegistrationViewText}
        </TextTemplate>
        <NavLink direction="left" href="/login">
          Back to Login
        </NavLink>
      </div>
    );
  },
});

const AccountInformation = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object,
    errors: React.PropTypes.object,
    accountInformation: React.PropTypes.object,
    blur: React.PropTypes.func,
    focus: React.PropTypes.func,
  },

  render: function() {
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessAccount = _accessSafe.bind(this, this.props.accountInformation);
    return (
      <div id="account_information">
        <h3>Account Information</h3>
        <RegistrationTextInput  
          errors={accessErrors('first_name')} 
          placeholder="First Name" 
          onChange={accessHandlers('first_name')} 
          value={accessAccount('first_name')} 
        />
        <RegistrationTextInput 
          errors={accessErrors('last_name')} 
          placeholder="Last Name" 
          onChange={accessHandlers('last_name')} 
          value={accessAccount('last_name')} 
        />
        <RegistrationTextInput
          errors={accessErrors('username')} 
          placeholder="Username" 
          onChange={accessHandlers('username')} 
          value={accessAccount('username')}
        />
        <RegistrationTextInput
          errors={accessErrors('password')} 
          type="password" 
          placeholder="Password" 
          value={accessAccount('password')} 
          onChange={accessHandlers('password')}
          onBlur={this.props.blur} 
          onFocus={this.props.focus} 
        />
        <RegistrationTextInput
          errors={accessErrors('password_confirm')} 
          type="password" 
          placeholder="Password (confirm)" 
          value={accessAccount('password_confirm')} 
          onChange={accessHandlers('password_confirm')} 
          onBlur={this.props.blur}
          onFocus={this.props.focus} 
        />
      </div>
    );
  },

});

const SchoolInformation = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object,
    errors: React.PropTypes.object,
    schoolInformation: React.PropTypes.object,
    handleInternationalChange: React.PropTypes.func,
    schoolInternational: React.PropTypes.bool,
  },

  render: function() {
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessSchool = _accessSafe.bind(this, this.props.schoolInformation);
    return (
      <div id="school_information">
        <h3>School Information</h3>
        <p className="instructions">Where is your school located?</p>
        <ul>
          <li>
            <label>
              <input 
                type="radio" 
                value=''
                onChange={this.props.handleInternationalChange} 
                checked={!this.props.schoolInternational}
              /> United States of America
            </label>
          </li>
          <li>
            <label>
              <input 
                type="radio" 
                value='international'
                onChange={this.props.handleInternationalChange} 
                checked={this.props.schoolInternational}
              /> International
            </label>
          </li>
        </ul>
        <RegistrationTextInput 
          errors={accessErrors('school_name')} 
          placeholder="Official School Name" 
          onChange={accessHandlers('school_name')} 
          value={accessSchool('school_name')} 
        />
        <RegistrationTextInput  
          errors={accessErrors('school_address')} 
          placeholder="Street Address" 
          onChange={accessHandlers('school_address')} 
          value={accessSchool('school_address')} 
        />
        <RegistrationTextInput  
          errors={accessErrors('school_city')} 
          placeholder="City" 
          onChange={accessHandlers('school_city')} 
          value={accessSchool('school_city')} 
        />
        <RegistrationTextInput  
          errors={accessErrors('school_state')} 
          placeholder="State" 
          onChange={accessHandlers('school_state')} 
          value={accessSchool('school_state')} 
        />
        <RegistrationTextInput  
          errors={accessErrors('school_zip')} 
          placeholder="Zip" 
          onChange={accessHandlers('school_zip')} 
          value={accessSchool('school_zip')} 
        />
        <RegistrationTextInput  
          errors={accessErrors('school_country')} 
          placeholder="Country" 
          onChange={accessHandlers('school_country')} 
          value={accessSchool('school_country')} 
          disabled={!this.props.schoolInternational} 
          isControlled={true} 
        />
      </div>
    );
  },

});

const ProgramInformation = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object,
    errors: React.PropTypes.object,
    programInformation: React.PropTypes.object,
    handleProgramTypeChange: React.PropTypes.func,
    programType: React.PropTypes.oneOf([ProgramTypes.CLUB,ProgramTypes.CLASS]),
  },

  render: function() {
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    var accessProgram = _accessSafe.bind(this, this.props.programInformation);
    return (
      <div id="program_information">
        <h3>Program Information</h3>
        <p className="instructions">What category best describes your program?</p>
        <ul>
          <li>
            <label>
              <input 
                type="radio" 
                checked={this.props.programType == ProgramTypes.CLUB} 
                value={ProgramTypes.CLUB} 
                onChange={this.props.handleProgramTypeChange}
              /> Club
            </label>
          </li>
          <li>
            <label>
              <input 
                type="radio" 
                value={ProgramTypes.CLASS} 
                checked={this.props.propTypes == ProgramTypes.CLASS} 
                onChange={this.props.handleProgramTypeChange} 
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
          Advanced: Attended more than seven conferences, has participated
          in many diverse committees.
        </label>
        {accessErrors('advanced_delegates')}
        <p className="instructions">
          Tentative Total Number of Delegates: {this._handleDelegateSum(
            accessProgram('beginner_delegates'), accessProgram('intermediate_delegates'), 
            accessProgram('advanced_delegates')
          )}
        </p>
      </div>
    );
  },

  _handleDelegateSum: function(beginner, intermediate, advanced) {
    var sum = 0;
    if (beginner) {
      sum += parseInt(beginner, 10) || 0;
    } if (intermediate) {
      sum += parseInt(intermediate, 10) || 0; 
    } if (advanced) {
      sum += parseInt(advanced, 10) || 0;
    }
    return sum;
  }

});

const PrimaryContact = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object,
    primaryContactInformation: React.PropTypes.object,
    errors: React.PropTypes.object,
    renderContactGenderField: React.PropTypes.func,
    renderContactTypeField: React.PropTypes.func,
    isInternational: React.PropTypes.bool,
  },

  render: function() {
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessPrimary = _accessSafe.bind(this, this.props.primaryContactInformation);
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    return (
      <div id='primary_contact'>
        <h3>Primary Contact</h3>
        {this.props.renderContactGenderField('primary_gender')}
        <RegistrationTextInput
          errors={accessErrors('primary_name')} 
          placeholder="Name" 
          onChange={accessHandlers('primary_name')} 
          value={accessPrimary('primary_name')} 
        />
        <RegistrationTextInput 
          errors={accessErrors('primary_email')} 
          placeholder="Email" 
          onChange={accessHandlers('primary_email')} 
          value={accessPrimary('primary_email')} 
        />
        <RegistrationTextInput 
          errors={accessErrors('primary_phone')} 
          onChange={accessHandlers('primary_phone')} 
          value={accessPrimary('primary_phone')} 
          placeholder="Phone Number" 
          isInternational={this.props.isInternational} 
        />
        {this.props.renderContactTypeField('primary_type')} 
      </div>
    );
  },
});

const SecondaryContact = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object,
    secondaryContactInformation: React.PropTypes.object,
    errors: React.PropTypes.object,
    renderContactGenderField: React.PropTypes.func,
    renderContactTypeField: React.PropTypes.func,
    isInternational: React.PropTypes.bool,
  },

  render: function() {
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessSecondary = _accessSafe.bind(this, this.props.secondaryContactInformation);
    var accessErrors = _accessSafe.bind(this, this.props.errors)
    return (
      <div id='secondary_contact'>
        <h3>Secondary Contact</h3>
        {this.props.renderContactGenderField('secondary_gender')}
        <RegistrationTextInput
          errors={accessErrors('secondary_name')}
          placeholder="Name" 
          onChange={accessHandlers('secondary_name')}
          value={accessSecondary('secondary_name')}
        />
        <RegistrationTextInput 
          errors={accessErrors('secondary_email')}
          placeholder="Email" 
          onChange={accessHandlers('secondary_email')}
          value={accessSecondary('secondary_email')}
        />
        <RegistrationTextInput 
          errors={accessErrors('secondary_phone')}
          onChange={accessHandlers('secondary_phone')}
          value={accessSecondary('secondary_phone')} 
          placeholder="Phone Number" 
          isInternational={this.props.isInternational}
        />
        {this.props.renderContactTypeField('secondary_type')}
      </div>
    );
  },

});

const CountryPreferences = React.createClass({
  propTypes: {
    renderCountryDropdown: React.PropTypes.func,
  },

  render: function() {
    return (
      <div id='country_preferences'>
        <h3>Country Preferences</h3>
        <p className="instructions">Please choose 10 United Nations Member States or
        Observers your school would like to represent. A reference list of
        countries and their relation to committees is
        available <a href="http://www.un.org/en/member-states/" target="_blank">online</a>.
        Please diversify your selection.</p>
        <ul>
          {this.props.renderCountryDropdown('01', 'country_pref1')}
          {this.props.renderCountryDropdown('02', 'country_pref2')}
          {this.props.renderCountryDropdown('03', 'country_pref3')}
          {this.props.renderCountryDropdown('04', 'country_pref4')}
          {this.props.renderCountryDropdown('05', 'country_pref5')}
          {this.props.renderCountryDropdown('06', 'country_pref6')}
          {this.props.renderCountryDropdown('07', 'country_pref7')}
          {this.props.renderCountryDropdown('08', 'country_pref8')}
          {this.props.renderCountryDropdown('09', 'country_pref9')}
          {this.props.renderCountryDropdown('10', 'country_pref10')}
        </ul>
      </div>
    );
  },

});

const SpecialCommitteePreferences = React.createClass({
  propTypes: {
    handlers: React.PropTypes.object, 
    errors: React.PropTypes.object, 
    specialCommitteePrefValues: React.PropTypes.object, 
    renderCommittees: React.PropTypes.func, 
  },

  render: function() {
    var accessHandlers = _accessSafe.bind(this, this.props.handlers);
    var accessErrors = _accessSafe.bind(this, this.props.errors);
    var accessValues = _accessSafe.bind(this, this.props.specialCommitteePrefValues);
    return (
      <div id='special_committee_preferences'>
        <h3>Special Committee Preferences</h3>
        <p className="instructions">Would your delegation be interested in
        being represented in the following small/specialized committees?
        Positions are limited and we may not be able to accommodate all
        preferences. You can find a reference to our
        committees <a href="http://www.bmun.org/committees" target="_blank">
        here</a>.</p>
        <ul>
          {this.props.renderCommittees()}
        </ul>
        <NumberInput 
          placeholder="Number of Spanish Speaking Delegates"  
          onChange={accessHandlers('spanish_speaking_delegates')} 
          value={accessValues('spanish_speaking_delegates')} 
        />
        {accessErrors('spanish_speaking_delegates')}
        <NumberInput 
          placeholder="Number of Chinese Speaking Delegates" 
          onChange={accessHandlers('chinese_speaking_delegates')} 
          value={accessValues('chinese_speaking_delegates')} 
        />
        {accessErrors('chinese_speaking_delegates')}
      </div>
    );
  },

});

const Comments = React.createClass({
  propTypes: {
    handler: React.PropTypes.func,
    value: React.PropTypes.string,
  },

  render: function() {
    return (
      <div id='comments'>
        <h3>Comments</h3>
        <p className="instructions">If there are any further details you
        would like us to know about your participation in BMUN this year or
        general feedback about the registration process, please comment
        below.</p>
        <textarea
          className="text-input"
          cols="40"
          rows="7"
          onChange={this.props.handler}
          value={this.props.value}
        />
      </div>
    );
  },

});

const RegistrationFooter = React.createClass({
  propTypes: {
    loading: React.PropTypes.bool,
  },

  render: function() {
    return (
      <div id='registration_footer'>
        <NavLink direction="left" href="/login">
          Back to Login
        </NavLink>
        <div style={{float: 'right'}}>
          <span className="help-text"><em>All done?</em></span>
          <Button
            color="green"
            loading={this.props.loading}
            type="submit">
            Register
          </Button>
        </div>
      </div>
    );
  },

});

module.exports = RegistrationView; 

