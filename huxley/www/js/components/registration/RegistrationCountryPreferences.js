/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from 'prop-types';

class RegistrationCountryPreferences extends React.Component {
  render() {
    return (
      <div id="country_preferences">
        <h3>Country Preferences</h3>
        <p className="instructions">
          Please choose 10 United Nations Member States or Observers your school
          would like to represent. A reference list of countries and their
          relation to committees is available{" "}
          <a href="http://www.un.org/en/member-states/" target="_blank">
            online
          </a>
          . Please diversify your selection.
        </p>
        <ul>
          {this.props.renderCountryDropdown("01", "country_pref1")}
          {this.props.renderCountryDropdown("02", "country_pref2")}
          {this.props.renderCountryDropdown("03", "country_pref3")}
          {this.props.renderCountryDropdown("04", "country_pref4")}
          {this.props.renderCountryDropdown("05", "country_pref5")}
          {this.props.renderCountryDropdown("06", "country_pref6")}
          {this.props.renderCountryDropdown("07", "country_pref7")}
          {this.props.renderCountryDropdown("08", "country_pref8")}
          {this.props.renderCountryDropdown("09", "country_pref9")}
          {this.props.renderCountryDropdown("10", "country_pref10")}
        </ul>
      </div>
    );
  }
}

(RegistrationCountryPreferences.propTypes = {
  renderCountryDropdown: PropTypes.func,
}),
  (module.exports = RegistrationCountryPreferences);
