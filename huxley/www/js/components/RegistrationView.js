/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import { history } from "utils/history";

const { StateTypes } = require("constants/StateTypes")
const { PaymentTypes } = require("constants/PaymentTypes");
const { Button } = require("components/core/Button");
const { CommitteeStore } = require("stores/CommitteeStore");
const { ContactTypes } = require("constants/ContactTypes");
const { CountrySelect } = require("components/CountrySelect");
const { CountryStore } = require("stores/CountryStore");
const { GenderConstants } = require("constants/GenderConstants");
const { NavLink } = require("components/NavLink");
const { OuterView } = require("components/OuterView");
const { ProgramTypes } = require("constants/ProgramTypes");
const {
  RegistrationAccountInformation,
} = require("components/registration/RegistrationAccountInformation");
const {
  RegistrationComments,
} = require("components/registration/RegistrationComments");
const {
  RegistrationCountryPreferences,
} = require("components/registration/RegistrationCountryPreferences");
const {
  RegistrationPrimaryContact,
} = require("components/registration/RegistrationPrimaryContact");
const {
  RegistrationProgramInformation,
} = require("components/registration/RegistrationProgramInformation");
const {
  RegistrationSchoolInformation,
} = require("components/registration/RegistrationSchoolInformation");
const {
  RegistrationSecondaryContact,
} = require("components/registration/RegistrationSecondaryContact");
const {
  RegistrationSpecialCommitteePreferences,
} = require("components/registration/RegistrationSpecialCommitteePreferences");
const RegistrationViewText = require("text/RegistrationViewText.md");
const { ServerAPI } = require("lib/ServerAPI");
const { ShakerContext } = require('components/Shaker');
const { StatusLabel } = require("components/core/StatusLabel");
const { TextTemplate } = require("components/core/TextTemplate");
const { _handleChange } = require("utils/_handleChange");
const {
  RegistrationPaymentInformation,
} = require("components/registration/RegistrationPaymentInformation")

require("css/RegistrationView.less");

const USA = "United States of America";

class RegistrationView extends React.Component {
  static contextType = ShakerContext;
  
  constructor(props) {
    super(props);
    this.state = {
      errors: {},
      countries: Object.values(CountryStore.getCountries()),
      committees: Object.values(CommitteeStore.getSpecialCommittees()),
      first_name: "",
      last_name: "",
      username: "",
      password: null,
      password2: null,
      school_name: "",
      school_address: "",
      school_city: "",
      school_state: StateTypes.ALABAMA,
      school_zip: "",
      school_country: "",
      school_international: false,
      program_type: ProgramTypes.CLUB,
      times_attended: "",
      num_beginner_delegates: "",
      num_intermediate_delegates: "",
      num_advanced_delegates: "",
      num_spanish_speaking_delegates: "",
      num_chinese_speaking_delegates: "",
      primary_name: "",
      primary_gender: GenderConstants.UNSPECFIED,
      primary_email: "",
      primary_phone: "",
      primary_type: ContactTypes.FACULTY,
      secondary_name: "",
      secondary_gender: GenderConstants.UNSPECFIED,
      secondary_email: "",
      secondary_phone: "",
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
      registration_comments: "",
      loading: false,
      passwordValidating: false,
      payment_type: PaymentTypes.CARD
    };
  }

  componentDidMount() {
    this._committeesToken = CommitteeStore.addListener(() => {
      this.setState({
        committees: Object.values(CommitteeStore.getSpecialCommittees()),
      });
    });

    this._countriesToken = CountryStore.addListener(() => {
      this.setState({ countries: Object.values(CountryStore.getCountries()) });
    });
  }

  componentWillUnmount() {
    this._committeesToken && this._committeesToken.remove();
    this._countriesToken && this._countriesToken.remove();
  }

  render() {
    return (
      <OuterView>
        <form id="registration" onSubmit={this._handleSubmit}>
          <div>
            <TextTemplate conferenceSession={global.conference.session}>
              {RegistrationViewText}
            </TextTemplate>
            <NavLink direction="left" href="/login">
              Back to Login
            </NavLink>
          </div>
          <hr />
          <RegistrationAccountInformation
            handlers={{
              first_name: _handleChange.bind(this, "first_name"),
              last_name: _handleChange.bind(this, "last_name"),
              username: _handleChange.bind(this, "username"),
              password: this._handlePasswordChange,
              password_confirm: this._handlePasswordConfirmChange,
            }}
            errors={{
              first_name: this.state.errors["first_name"],
              last_name: this.state.errors["last_name"],
              username: this.state.errors["username"],
              password: this.state.errors["password"],
              password_confirm: this._getPasswordConfirmError(),
            }}
            accountInformation={{
              first_name: this.state.first_name,
              last_name: this.state.last_name,
              username: this.state.username,
              password: this.state.password,
              password_confirm: this.state.password2,
            }}
            blur={this._handlePasswordBlur}
            focus={this._handlePasswordFocus}
          />
          <hr />
          <RegistrationSchoolInformation
            handlers={{
              school_name: _handleChange.bind(this, "school_name"),
              school_address: _handleChange.bind(this, "school_address"),
              school_city: _handleChange.bind(this, "school_city"),
              school_state: _handleChange.bind(this, "school_state"),
              school_zip: _handleChange.bind(this, "school_zip"),
              school_country: _handleChange.bind(this, "school_country"),
            }}
            errors={{
              school_name: this._getSchoolErrors("name"),
              school_address: this._getSchoolErrors("address"),
              school_city: this._getSchoolErrors("city"),
              school_state: this._getSchoolErrors("state"),
              school_zip: this._getSchoolErrors("zip_code"),
              school_country: this._getSchoolErrors("country"),
            }}
            schoolInformation={{
              school_name: this.state.school_name,
              school_address: this.state.school_address,
              school_city: this.state.school_city,
              school_state: this.state.school_state,
              school_zip: this.state.school_zip,
              school_country: this._getSchoolCountry(),
            }}
            handleInternationalChange={this._handleInternationalChange}
            schoolInternational={this.state.school_international}
            renderStateTypesDropdown = {this.renderStateTypesDropdown}
          />
          <hr />
          <RegistrationProgramInformation
            handlers={{
              times_attended: _handleChange.bind(this, "times_attended"),
              num_beginner_delegates: _handleChange.bind(
                this,
                "num_beginner_delegates"
              ),
              num_intermediate_delegates: _handleChange.bind(
                this,
                "num_intermediate_delegates"
              ),
              num_advanced_delegates: _handleChange.bind(
                this,
                "num_advanced_delegates"
              ),
            }}
            errors={{
              times_attended: this.renderSchoolError("times_attended"),
              num_beginner_delegates: this.renderError(
                "num_beginner_delegates"
              ),
              num_intermediate_delegates: this.renderError(
                "num_intermediate_delegates"
              ),
              num_advanced_delegates: this.renderError(
                "num_advanced_delegates"
              ),
            }}
            programInformation={{
              times_attended: this.state.times_attended,
              num_beginner_delegates: this.state.num_beginner_delegates,
              num_intermediate_delegates: this.state.num_intermediate_delegates,
              num_advanced_delegates: this.state.num_advanced_delegates,
            }}
            handleProgramTypeChange={this._handleProgramTypeChange}
            programType={this.state.program_type}
          />
          <hr />
          <RegistrationPrimaryContact
            handlers={{
              primary_name: _handleChange.bind(this, "primary_name"),
              primary_email: _handleChange.bind(this, "primary_email"),
              primary_phone: this._handlePrimaryPhoneChange,
            }}
            errors={{
              primary_name: this._getSchoolErrors("primary_name"),
              primary_email: this._getSchoolErrors("primary_email"),
              primary_phone: this._getSchoolErrors("primary_phone"),
            }}
            primaryContactInformation={{
              primary_name: this.state.primary_name,
              primary_email: this.state.primary_email,
              primary_phone: this.state.primary_phone,
            }}
            renderContactGenderField={this.renderContactGenderField}
            renderContactTypeField={this.renderContactTypeField}
            isInternational={this.state.school_international}
          />
          <hr />
          <RegistrationSecondaryContact
            handlers={{
              secondary_name: _handleChange.bind(this, "secondary_name"),
              secondary_email: _handleChange.bind(this, "secondary_email"),
              secondary_phone: this._handleSecondaryPhoneChange,
            }}
            errors={{
              secondary_name: this._getSchoolErrors("secondary_name"),
              secondary_email: this._getSchoolErrors("secondary_email"),
              secondary_phone: this._getSchoolErrors("secondary_phone"),
            }}
            secondaryContactInformation={{
              secondary_name: this.state.secondary_name,
              secondary_email: this.state.secondary_email,
              secondary_phone: this.state.secondary_phone,
            }}
            renderContactGenderField={this.renderContactGenderField}
            renderContactTypeField={this.renderContactTypeField}
            isInternational={this.state.school_international}
          />
          <hr />
          <RegistrationCountryPreferences
            renderCountryDropdown={this.renderCountryDropdown}
          />
          <hr />
          <RegistrationSpecialCommitteePreferences
            handlers={{
              num_spanish_speaking_delegates: _handleChange.bind(
                this,
                "num_spanish_speaking_delegates"
              ),
              num_chinese_speaking_delegates: _handleChange.bind(
                this,
                "num_chinese_speaking_delegates"
              ),
            }}
            errors={{
              num_spanish_speaking_delegates: this.renderError(
                "num_spanish_speaking_delegates"
              ),
              num_chinese_speaking_delegates: this.renderError(
                "num_chinese_speaking_delegates"
              ),
            }}
            specialCommitteePrefValues={{
              num_spanish_speaking_delegates: this.state
                .num_spanish_speaking_delegates,
              num_chinese_speaking_delegates: this.state
                .num_chinese_speaking_delegates,
            }}
            renderCommittees={this.renderCommittees}
          />
          <hr />
          <RegistrationPaymentInformation
            handlers={{
              payment_type: _handleChange.bind(this, "payment_type"),
            }}
            errors={{
              payment_type: this.renderError("payment_type"),
            }}
            paymentInformation={{
              payment_type: this.state.payment_type, 
            }}
            handlePaymentTypeChange={this._handlePaymentTypeChange}
            paymentType={this.state.payment_type}
          />
          <hr />
          <RegistrationComments
            handler={_handleChange.bind(this, "registration_comments")}
            value={this.state.registration_comments}
          />
          <hr />
          <div id="registration_footer">
            <NavLink direction="left" href="/login">
              Back to Login
            </NavLink>
            <div style={{ float: "right" }}>
              <span className="help-text">
                <em>All done?</em>
              </span>
              <Button color="green" loading={this.state.loading} type="submit">
                Register
              </Button>
            </div>
          </div>
        </form>
      </OuterView>
    );
  }

  renderCountryDropdown = (labelNum, fieldName) => {
    return (
      <li>
        <label>{labelNum}</label>
        <CountrySelect
          onChange={_handleChange.bind(this, fieldName)}
          countries={this.state.countries.sort((country) => country.name)}
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
            this.state.country_pref10,
          ]}
        />
      </li>
    );
  };

  renderCommittees = () => {
    return this.state.committees.map(function (committee) {
      return (
        <li key={committee.id}>
          <label name="committee_prefs">
            <input
              className="choice"
              type="checkbox"
              name="committee_prefs"
              onChange={this._handleCommitteePreferenceChange.bind(
                this,
                committee
              )}
            />
            {committee.full_name}
          </label>
        </li>
      );
    }, this);
  };

  renderContactGenderField = (name) => {
    return (
      <select
        className="contact-select reg-field"
        onChange={_handleChange.bind(this, name)}
        value={this.state[name]}
      >
        <option
          key={GenderConstants.UNSPECFIED}
          value={GenderConstants.UNSPECFIED}
        >
          Unspecified
        </option>
        <option key={GenderConstants.MALE} value={GenderConstants.MALE}>
          Mr.
        </option>
        <option key={GenderConstants.FEMALE} value={GenderConstants.FEMALE}>
          Mrs./Ms.
        </option>
        <option key={GenderConstants.OTHER} value={GenderConstants.OTHER}>
          Other
        </option>
      </select>
    );
  };

  renderContactTypeField = (name) => {
    return (
      <select
        className="contact-select reg-field"
        onChange={_handleChange.bind(this, name)}
        value={this.state[name]}
      >
        <option key={ContactTypes.STUDENT} value={ContactTypes.STUDENT}>
          Student
        </option>
        <option key={ContactTypes.FACULTY} value={ContactTypes.FACULTY}>
          Faculty
        </option>
      </select>
    );
  };

  renderStateTypesDropdown = (name) => {
    return (
      <select
        className="state-select reg-field"
        onChange={_handleChange.bind(this, name)}
        value={this.state[name]}
      > 
        <option key={StateTypes.ALABAMA} value={StateTypes.ALABAMA}> Alabama </option>
        <option key={StateTypes.ALASKA} value={StateTypes.ALASKA}> Alaska </option>
        <option key={StateTypes.AMERICAN_SAMOA} value={StateTypes.AMERICAN_SAMOA}> American Samoa </option>
        <option key={StateTypes.ARIZONA} value={StateTypes.ARIZONA}> Arizona </option>
        <option key={StateTypes.ARKANSAS} value={StateTypes.ARKANSAS}> Arkansas </option>
        <option key={StateTypes.CALIFORNIA} value={StateTypes.CALIFORNIA}> California </option>
        <option key={StateTypes.COLORADO} value={StateTypes.COLORADO}> Colorado </option>
        <option key={StateTypes.CONNECTICUT} value={StateTypes.CONNECTICUT}> Connecticut </option>
        <option key={StateTypes.DELAWARE} value={StateTypes.DELAWARE}> Delaware </option>
        <option key={StateTypes.DISTRICT_OF_COLUMBIA} value={StateTypes.DISTRICT_OF_COLUMBIA}> District of Columbia </option>
        <option key={StateTypes.FLORIDA} value={StateTypes.FLORIDA}> Florida </option>
        <option key={StateTypes.GEORGIA} value={StateTypes.GEORGIA}> Georgia </option>
        <option key={StateTypes.GUAM} value={StateTypes.GUAM}> Guam </option>
        <option key={StateTypes.HAWAII} value={StateTypes.HAWAII}> Hawaii </option>
        <option key={StateTypes.IDAHO} value={StateTypes.IDAHO}> Idaho </option>
        <option key={StateTypes.ILLINOIS} value={StateTypes.ILLINOIS}> Illinois </option>
        <option key={StateTypes.INDIANA} value={StateTypes.INDIANA}> Indiana </option>
        <option key={StateTypes.IOWA} value={StateTypes.IOWA}> Iowa </option>
        <option key={StateTypes.KANSAS} value={StateTypes.KANSAS}> Kansas </option>
        <option key={StateTypes.KENTUCKY} value={StateTypes.KENTUCKY}> Kentucky </option>
        <option key={StateTypes.LOUISIANA} value={StateTypes.LOUISIANA}> Louisiana </option>
        <option key={StateTypes.MAINE} value={StateTypes.MAINE}> Maine </option>
        <option key={StateTypes.MARYLAND} value={StateTypes.MARYLAND}> Maryland </option>
        <option key={StateTypes.MASSACHUSETTS} value={StateTypes.MASSACHUSETTS}> Massachusetts </option>
        <option key={StateTypes.MICHIGAN} value={StateTypes.MICHIGAN}> Michigan </option>
        <option key={StateTypes.MINNESOTA} value={StateTypes.MINNESOTA}> Minnesota </option>
        <option key={StateTypes.MISSISSIPPI} value={StateTypes.MISSISSIPPI}> Mississippi </option>
        <option key={StateTypes.MISSOURI} value={StateTypes.MISSOURI}> Missouri </option>
        <option key={StateTypes.MONTANA} value={StateTypes.MONTANA}> Montana </option>
        <option key={StateTypes.NEBRASKA} value={StateTypes.NEBRASKA}> Nebraska </option>
        <option key={StateTypes.NEVADA} value={StateTypes.NEVADA}> Nevada </option>
        <option key={StateTypes.NEW_HAMPSHIRE} value={StateTypes.NEW_HAMPSHIRE}> New Hampshire </option>
        <option key={StateTypes.NEW_JERSEY} value={StateTypes.NEW_JERSEY}> New Jersey </option>
        <option key={StateTypes.NEW_MEXICO} value={StateTypes.NEW_MEXICO}> New Mexico </option>
        <option key={StateTypes.NEW_YORK} value={StateTypes.NEW_YORK}> New York </option>
        <option key={StateTypes.NORTH_CAROLINA} value={StateTypes.NORTH_CAROLINA}> North Carolina </option>
        <option key={StateTypes.NORTH_DAKOTA} value={StateTypes.NORTH_DAKOTA}> North Dakota </option>
        <option key={StateTypes.NORTHERN_MARIANA_IS} value={StateTypes.NORTHERN_MARIANA_IS}> Northern Mariana Islands </option>
        <option key={StateTypes.OHIO} value={StateTypes.OHIO}> Ohio </option>
        <option key={StateTypes.OKLAHOMA} value={StateTypes.OKLAHOMA}> Oklahoma </option>
        <option key={StateTypes.OREGON} value={StateTypes.OREGON}> Oregon </option>
        <option key={StateTypes.PENNSYLVANIA} value={StateTypes.PENNSYLVANIA}> Pennsylvania </option>
        <option key={StateTypes.PUERTO_RICO} value={StateTypes.PUERTO_RICO}> Puerto Rico </option>
        <option key={StateTypes.RHODE_ISLAND} value={StateTypes.RHODE_ISLAND}> Rhode Island </option>
        <option key={StateTypes.SOUTH_CAROLINA} value={StateTypes.SOUTH_CAROLINA}> South Carolina </option>
        <option key={StateTypes.SOUTH_DAKOTA} value={StateTypes.SOUTH_DAKOTA}> South Dakota </option>
        <option key={StateTypes.TENNESSEE} value={StateTypes.TENNESSEE}> Tennessee </option>
        <option key={StateTypes.TEXAS} value={StateTypes.TEXAS}> Texas </option>
        <option key={StateTypes.UTAH} value={StateTypes.UTAH}> Utah </option>
        <option key={StateTypes.VERMONT} value={StateTypes.VERMONT}> Vermont </option>
        <option key={StateTypes.VIRGINIA} value={StateTypes.VIRGINIA}> Virginia </option>
        <option key={StateTypes.VIRGIN_ISLANDS} value={StateTypes.VIRGIN_ISLANDS}> Virgin Islands </option>
        <option key={StateTypes.WASHINGTON} value={StateTypes.WASHINGTON}> Washington </option>
        <option key={StateTypes.WEST_VIRGINIA} value={StateTypes.WEST_VIRGINIA}> West Virginia </option>
        <option key={StateTypes.WISCONSIN} value={StateTypes.WISCONSIN}> Wisconsin </option>
        <option key={StateTypes.WYOMING} value={StateTypes.WYOMING}> Wyoming </option>
      </select>
    )

  }

  renderError = (field) => {
    if (this.state.errors[field]) {
      return (
        <StatusLabel status="error">{this.state.errors[field]}</StatusLabel>
      );
    }

    return null;
  };

  _getPasswordConfirmError = () => {
    if (
      this.state.passwordValidating &&
      this.state.password !== this.state.password2
    ) {
      return ["Please enter the same password again."];
    }
  };

  renderSchoolError = (field) => {
    if (this.state.errors.school && this.state.errors.school[field]) {
      return (
        <StatusLabel status="error">
          {this.state.errors.school[field]}
        </StatusLabel>
      );
    }

    return null;
  };

  _getSchoolErrors = (field) => {
    if (this.state.errors.school) {
      return this.state.errors.school[field];
    }
  };

  _handleDelegateSum = () => {
    var sum = 0;
    if (this.state.num_beginner_delegates) {
      sum += parseInt(this.state.num_beginner_delegates, 10) || 0;
    }
    if (this.state.num_intermediate_delegates) {
      sum += parseInt(this.state.num_intermediate_delegates, 10) || 0;
    }
    if (this.state.num_advanced_delegates) {
      sum += parseInt(this.state.num_advanced_delegates, 10) || 0;
    }
    return sum;
  };

  _handlePasswordBlur = () => {
    this.setState({ passwordValidating: true });
  };

  _handlePasswordFocus = () => {
    this.setState({ passwordValidating: false });
  };

  _handleProgramTypeChange = (event) => {
    this.setState({ program_type: parseInt(event.target.value) });
  };

  _handlePaymentTypeChange = (event) => {
    this.setState({ payment_type: parseInt(event.target.value) });
  };


  _handleCommitteePreferenceChange = (committee) => {
    var index = this.state.committee_prefs.indexOf(committee.id);
    if (index < 0) {
      this.setState({
        committee_prefs: this.state.committee_prefs.concat(committee.id),
      });
    } else {
      this.setState({
        committee_prefs: this.state.committee_prefs.filter(function (id) {
          return committee.id !== id;
        }),
      });
    }
  };

  _handleInternationalChange = (event) => {
    this.setState({ school_international: !!event.target.value });
  };

  _handlePrimaryPhoneChange = (number) => {
    this.setState({ primary_phone: number });
  };

  _handleSecondaryPhoneChange = (number) => {
    this.setState({ secondary_phone: number });
  };

  _handlePasswordChange = (password) => {
    this.setState({ password });
  };

  _handlePasswordConfirmChange = (password2) => {
    this.setState({ password2 });
  };

  _getSchoolCountry = () => {
    return this.state.school_international ? this.state.school_country : USA;
  };

  _handleSubmit = (event) => {
    this.setState({ loading: true });
    ServerAPI.register({
      user: {
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
        },
      },
      registration: {
        conference: global.conference.session,
        num_beginner_delegates: this.state.num_beginner_delegates,
        num_intermediate_delegates: this.state.num_intermediate_delegates,
        num_advanced_delegates: this.state.num_advanced_delegates,
        num_spanish_speaking_delegates: this.state
          .num_spanish_speaking_delegates,
        num_chinese_speaking_delegates: this.state
          .num_chinese_speaking_delegates,
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
          this.state.country_pref10,
        ],
        payment_type: this.state.payment_type,
        committee_preferences: this.state.committee_prefs,
        registration_comments: this.state.registration_comments.trim(),
      },
    }).then(this._handleSuccess, this._handleError);
    event.preventDefault();
  };

  _handleSuccess = (response) => {
    if (response.registration.is_waitlisted) {
      history.redirect("/register/waitlist");
    } else {
      history.redirect("/register/success");
    }
  };

  _handleError = (response) => {
    if (!response) {
      return;
    }

    this.setState(
      {
        errors: response,
        loading: false,
      },
      () => {
        this.context && this.context();
      }
    );
  };
}

export { RegistrationView };
