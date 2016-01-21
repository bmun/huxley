/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react/addons');

var CountrySelect = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    countries: React.PropTypes.array,
    selectedCountryID: React.PropTypes.number,
    countryPreferences: React.PropTypes.array
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
      var index = this.props.countryPreferences.indexOf(""+country.id)
      if(index < 0){
        return (
          <option key={country.id} value={country.id}>
            {country.name}
          </option>
        );

      }else{
        return (
          <option key={country.id} value={country.id} disabled>
            {country.name}
          </option>
        );
      }
    }.bind(this));
  }
});

module.exports = CountrySelect;
