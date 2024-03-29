/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";

class CountrySelect extends React.Component {
  shouldComponentUpdate(nextProps, nextState) {
    for (var i = 0; i < this.props.countryPreferences.length; i++) {
      if (
        this.props.countryPreferences[i] !== nextProps.countryPreferences[i]
      ) {
        return true;
      }
    }
    return (
      nextProps.selectedCountryID !== this.props.selectedCountryID ||
      nextProps.countries.length !== this.props.countries.length
    );
  }

  render() {
    return (
      <select
        onChange={this.props.onChange}
        value={this.props.selectedCountryID}
      >
        <option value="0">No Preference</option>
        {this.renderCommitteeOptions()}
      </select>
    );
  }

  renderCommitteeOptions = () => {
    return this.props.countries.map(
      function (country) {
        if (!country.special) {
          var index = this.props.countryPreferences.indexOf("" + country.id);
          return (
            <option key={country.id} value={country.id} disabled={index >= 0}>
              {country.name}
            </option>
          );
        }
      }.bind(this)
    );
  };
}

CountrySelect.propTypes = {
  onChange: PropTypes.func,
  countries: PropTypes.array,
  selectedCountryID: PropTypes.number,
  countryPreferences: PropTypes.array,
};

export { CountrySelect };
