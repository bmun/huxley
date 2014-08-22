/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');

var CountrySelect = React.createClass({

  render: function() {
    return (
      <select
        onChange={this.props.onChange}
        value={this.props.selectedCountryID}
        className="country-select">
        <option value="0">No Preference</option>
        {this.props.countries}
      </select>
    );
  }
});

module.exports = CountrySelect;
