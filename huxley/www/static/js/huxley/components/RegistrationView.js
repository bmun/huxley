/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var console = require('console');

var $ = require('jquery');
var Link = require('react-router-component').Link;
var React = require('react/addons');

var CurrentUserActions = require('../actions/CurrentUserActions');
var OuterView = require('./OuterView');
var CountryStore = require('../stores/CountryStore');

require('jquery-ui/effect-shake');

var RegistrationView = React.createClass({
  mixins: [React.addons.LinkedStateMixin],

  getInitialState: function() {
    return {
      error: null,
      countries: [],
      first_name: null,
      last_name: null,
      username: null,
      password: null,
      password2: null,
      school_name: null,
      school_address: null,
      school_state: null,
      shool_zip: null,
      school_country: "United States of America",
      program_type: "Club",
      times_attended: null,
      min_delegation_size: null,
      max_delegation_size: null,
      primary_name: null,
      primary_email: null,
      primary_phone: null,
      secondary_name: null,
      secondary_email: null,
      secondary_phone: null,
      country_pref1: null,
      country_pref2: null,
      country_pref3: null,
      country_pref4: null,
      country_pref5: null,
      country_pref6: null,
      country_pref7: null,
      country_pref8: null,
      country_pref9: null,
      country_pref10: null,
      committee_prefs: null,
      loading: false
    };
  },

  countryOption: function(currentValue, index, array) {
    var option = document.createElement('OPTION');
    option.text = currentValue.name;
    return option;
  },

  addOption: function(array, number) {
    for (var x = 0; x<array.length; x++) {
      array[x].value='country_pref'+String(number);
      array[x] = React.DOM.option(array[x]);
    }
    return array
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
            <Link
              className="outer-nav arrow-left"
              href="/login">
              Back to Login
            </Link>
          </div>
          <div className="registration-fields">
            <hr><h3>Account Information</h3></hr>
            <input
              className="text"
              type="text"
              name="first_name"
              placeholder="First Name"
              valueLink={this.linkState('first_name')}
            />
            <input
              className="text"
              type="text"
              name="last_name"
              placeholder="Last Name"
              valueLink={this.linkState('last_name')}
            />
            <input
              className="text"
              type="text"
              name="username"
              placeholder="Username"
              valueLink={this.linkState('username')}
            />
            <input
              className="text"
              type="password"
              name="password"
              placeholder="Password"
              valueLink={this.linkState('password')}
            />
            <input
              className="text"
              type="password"
              name="password2"
              placeholder="Password (confirm)"
              valueLink={this.linkState('password2')}
            />
            <h3><hr>School Information</hr></h3>
            <p className="instructions">Where is your school located?</p>
            <input
              className="choice"
              type="radio"
              name="school_location"
              valueLink={this.linkState("United States of America")}
              checked="true"
            /> United States of America <br></br>
            <input
              className="choice"
              type="radio"
              name="school_location"
              valueLink={this.linkState("International")}
            /> International <br></br>
            <input
              className="text"
              type="text"
              name="school_name"
              placeholder="Official School Name"
              valueLink={this.linkState('school_name')}
            />
            <input
              className="text"
              type="text"
              name="school_address"
              placeholder="Street Address"
              valueLink={this.linkState('school_address')}
            />
            <input
              className="text"
              type="text"
              name="school_city"
              placeholder="City"
              valueLink={this.linkState('school_city')}
            />
            <input
              className="text"
              type="text"
              name="school_state"
              placeholder="State"
              valueLink={this.linkState('school_state')}
            />
            <input
              className="text"
              type="text"
              name="school_zip"
              placeholder="Zip"
              valueLink={this.linkState('school_zip')}
            />
            <input
              className="text"
              type="text"
              name="school_country"
              placeholder="Country"
              valueLink={this.linkState('school_country')}
            />
            <h3><hr>Program Information</hr></h3>
            <p className="instructions">What category best describes your program?</p>
            <input
              className="choice"
              type="radio"
              name="program_type"
              checked="true"
              valueLink={this.linkState("Club")}
            /> Club <br></br>
            <input
              className="choice"
              type="radio"
              name="program_type"
              valueLink={this.linkState("Class")}
            /> Class <br></br>
            <p className="instructions">Please tell us a bit more about your delegation this
              year.</p>
            <input
              className="text"
              type="text"
              name="times_attended"
              placeholder="Number of BMUN sessions attended"
              valueLink={this.linkState("times_attended")}
            />
            <input
              className="text"
              type="text"
              name="min_delegation_size"
              placeholder="Minimum Delegation Size"
              valueLink={this.linkState('min_delegation_size')}
            />
            <input
              className="text"
              type="text"
              name="max_delegation_size"
              placeholder="Maximum Delegation Size"
              valueLink={this.linkState('max_delegation_size')}
            />
            <h3><hr>Primary Contact</hr></h3>
            <input
              className="text"
              type="text"
              name="primary_name"
              placeholder="Name"
              valueLink={this.linkState('primary_name')}
            />
            <input
              className="text"
              type="text"
              name="primary_email"
              placeholder="Email"
              valueLink={this.linkState('primary_email')}
            />
            <input
              className="text"
              type="text"
              name="primary_phone"
              placeholder="Phone Number"
              valueLink={this.linkState('primary_phone')}
            />
            <h3><hr>Secondary Contact</hr></h3>
            <input
              className="text"
              type="text"
              name="secondary_name"
              placeholder="Name"
              valueLink={this.linkState('secondary_name')}
            />
            <input
              className="text"
              type="text"
              name="secondary_email"
              placeholder="Email"
              valueLink={this.linkState('secondary_email')}
            />
            <input
              className="text"
              type="text"
              name="secondary_phone"
              placeholder="Phone Number"
              valueLink={this.linkState('secondary_phone')}
            />
            <h3><hr>Country Preferences</hr></h3>
            <p className="instructions">Please choose 10 United Nations Member States or
            Observers your school would like to represent. A reference list of
            countries and their relation to committees is available online.
            Please diversify your selection.</p>
            <ul>
              <li>
                <label>01</label>
                <select name="country_pref1">
                  <option selected="true">No Preference</option>
                  {this.addOption(this.state.countries.map(this.countryOption), 1)}
                </select>
              </li>
              <li>
                <label>02</label>
                <select name="country_pref2">
                  <option selected="true"> No Preference</option>
                  {this.addOption(this.state.countries.map(this.countryOption), 2)}
                </select>
              </li>
              <li>
                <label>03</label>
                <select name="country_pref2">
                  <option selected="true"> No Preference</option>
                  {this.addOption(this.state.countries.map(this.countryOption), 3)}
                </select>
              </li>
              <li>
                <label>04</label>
                <select name="country_pref2">
                  <option selected="true"> No Preference</option>
                  {this.addOption(this.state.countries.map(this.countryOption), 4)}
                </select>
              </li>
              <li>
                <label>05</label>
                <select name="country_pref2">
                  <option selected="true"> No Preference</option>
                  {this.addOption(this.state.countries.map(this.countryOption), 5)}
                </select>
              </li>
              <li>
                <label>06</label>
                <select name="country_pref2">
                  <option selected="true"> No Preference</option>
                  {this.addOption(this.state.countries.map(this.countryOption), 6)}
                </select>
              </li>
              <li>
                <label>07</label>
                <select name="country_pref2">
                  <option selected="true"> No Preference</option>
                  {this.addOption(this.state.countries.map(this.countryOption), 7)}
                </select>
              </li>
              <li>
                <label>08</label>
                <select name="country_pref2">
                  <option selected="true"> No Preference</option>
                  {this.addOption(this.state.countries.map(this.countryOption), 8)}
                </select>
              </li>
              <li>
                <label>09</label>
                <select name="country_pref2">
                  <option selected="true"> No Preference</option>
                  {this.addOption(this.state.countries.map(this.countryOption), 9)}
                </select>
              </li>
              <li>
                <label>10</label>
                <select name="country_pref2">
                  <option selected="true"> No Preference</option>
                  {this.addOption(this.state.countries.map(this.countryOption), 10)}
                </select>
              </li>
            </ul>
            <h3><hr>Special Committee Preferences</hr></h3>
            <p className="instructions">Would your delegation be interested in being represented
            in the following small/specialized committees? Positions are limited
            and we may not be able to accomodate all preferences.</p>
            <input
              className="choice"
              type="checkbox"
              name="committee_prefs"
              valueLink={this.linkState('Crisis Simulation')}
            /> Crisis Simulation <br></br>
            <input
              className="choice"
              type="checkbox"
              name="committee_prefs"
              valueLink={this.linkState('Historical Security Council')}
            /> Historical Security Council <br></br>
            <input
              className="choice"
              type="checkbox"
              name="committee_prefs"
              valueLink={this.linkState('International Court of Justice')}
            /> International Court of Justice <br></br>
            <input
              className="choice"
              type="checkbox"
              name="committee_prefs"
              valueLink={this.linkState('North Atlantic Treaty Organization')}
            /> North Atlantic Treaty Organization <br></br>
            <input
              className="choice"
              type="checkbox"
              name="committee_prefs"
              valueLink={this.linkState('Organization of American States')}
            /> Organization of American States <br></br>
            <input
              className="choice"
              type="checkbox"
              name="committee_prefs"
              valueLink={this.linkState('Press Corp.')}
            /> Press Corp. <br></br>
            <input
              className="choice"
              type="checkbox"
              name="committee_prefs"
              valueLink={this.linkState('Security Council')}
            /> Security Council <br></br>
            <hr></hr>
              <Link
                className="outer-nav arrow-left"
                href="/login">
                Back to Login
              </Link>
              <span className="help-text"><em>All done?</em></span>
              <button
                className={cx({
                  'button':true,
                  'button-green':true,
                  'rounded-small':true
                })}
                type="submit">
                <span>Register</span>
              </button>
          </div>
        </form>
      </OuterView>
    );
  },

  _handleSubmit: function(event) {
    this.setState({loading: true});
    $.ajax({
      type: 'POST',
      url: '/api/users/me',
      data: {
        first_name: this.state.first_name,
        last_name: this.state.last_name,
        username: this.state.username,
        password: this.state.password,
        password2: this.state.password2,
        school_name: this.state.school_name,
        school_address: this.state.school_address,
        school_state: this.state.school_state,
        school_zip: this.state.school_zip,
        school_country: this.state.school_country,
        program_type: this.state.program_type,
        times_attended: this.state.times_attended,
        min_delegation_size: this.state.min_delegation_size,
        max_delegation_size: this.state.max_delegation_size,
        primary_name: this.state.primary_name,
        primary_email: this.state.primary_email,
        primary_phone: this.state.primary_phone,
        secondary_name: this.state.secondary_name,
        secondary_email: this.state.secondary_email,
        secondary_phone: this.state.secondary_phone,
        country_pref1: this.state.country_pref1,
        country_pref2: this.state.country_pref2,
        country_pref3: this.state.country_pref3,
        country_pref4: this.state.country_pref4,
        country_pref5: this.state.country_pref5,
        country_pref6: this.state.country_pref6,
        country_pref7: this.state.country_pref7,
        country_pref8: this.state.country_pref8,
        country_pref9: this.state.country_pref9,
        country_pref10: this.state.country_pref10,
        committee_prefs: this.state.committee_prefs
      },
      success: this._handleSuccess,
      error: this._handleError,
      dataType: 'json'
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    CurrentUserActions.login(jqXHR.responseJSON);
  },

  _handleError: function(jqXHR, status, error) {
    var response = jqXHR.responseJSON;
    if (!response.detail) {
      return;
    }

    this.setState({
      error: response.detail,
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
