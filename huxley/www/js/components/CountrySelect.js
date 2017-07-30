/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var CountrySelect = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    countries: React.PropTypes.array,
    selectedCountryID: React.PropTypes.number,
    countryPreferences: React.PropTypes.array,
  },

  shouldComponentUpdate: function(nextProps, nextState) {
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
  },

  render: function() {
    return (
      <select
        onChange={this.props.onChange}
        value={this.props.selectedCountryID}>
        <option value="0">No Preference</option>
        {this.renderCommitteeOptions()}
      </select>
    );
  },

  renderCommitteeOptions: function() {
    return this.props.countries.map(
      function(country) {
        if (!country.special) {
          var index = this.props.countryPreferences.indexOf('' + country.id);
          return (
            <option key={country.id} value={country.id} disabled={index >= 0}>
              {country.name}
            </option>
          );
        }
      }.bind(this),
    );
  },
});

module.exports = CountrySelect;
