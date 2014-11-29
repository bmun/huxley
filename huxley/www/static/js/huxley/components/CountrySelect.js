/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react/addons');

var CountrySelect = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    countries: React.PropTypes.array,
    selectedCountryID: React.PropTypes.number
  },

  shouldComponentUpdate: function(nextProps, nextState) {
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
    return this.props.countries.map(function(country) {
      return (
        <option key={country.id} value={country.id}>
          {country.name}
        </option>
      );
    });
  }
});

module.exports = CountrySelect;
