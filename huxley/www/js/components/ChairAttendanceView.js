/**
* Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var AssignmentStore = require('stores/AssignmentStore');
var Button = require('components/Button');
var CommitteeStore = require('stores/CommitteeStore');
var ConferenceContext = require('components/ConferenceContext');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var CurrentUserActions = require('actions/CurrentUserActions');
var DelegateSelect = require('components/DelegateSelect');
var DelegateStore = require('stores/DelegateStore');
var InnerView = require('components/InnerView');
var PermissionDeniedView = require('components/PermissionDeniedView');
var ServerAPI = require('lib/ServerAPI');
var User = require('utils/User');

var ChairAttendanceView = React.createClass({

  getInitialState: function() {
    return {
      countries: [],
    };
  },

  mixins: [
    ReactRouter.History,
  ],

  componentWillMount: function() {
    var user = CurrentUserStore.getCurrentUser();
     CountryStore.getCountries(function(countries) {
      this.setState({countries: countries});
    }.bind(this));

    if (!User.isChair(user)) {
      this.history.pushState(null, '/');
    }
  },

  renderAttendanceRows: function() {
    return this.state.countries.map(function(country) {
      return (
        <tr>
          <td>
            {country.name}
          </td>
          <td>
              <label name="committee_prefs">
                <input
                  className="choice"
                  type="checkbox"
                  name="committee_prefs"
                />
              </label>
          </td>
          <td>
              <label name="committee_prefs">
                <input
                  className="choice"
                  type="checkbox"
                  name="committee_prefs"
                />
              </label>
          </td>
          <td>
              <label name="committee_prefs">
                <input
                  className="choice"
                  type="checkbox"
                  name="committee_prefs"
                />
              </label>
          </td>
        </tr>
      )}.bind(this));
  },

  render: function() {
      return (
        <InnerView>
          <h2>Attendance</h2>
          <p>
            Here you can take attendance for delegates. Note that confirming attendance will alert
            the advisor as to if there delegates have shown up to committee.
          </p>
            <form>
            <div className="table-container">
              <table className="table highlight-cells">
                <thead>
                  <tr>
                    <th>Assignment</th>
                    <th>Present</th>
                    <th>Present2</th>
                    <th>Present3</th>
                  </tr>
                </thead>
                <tbody>
                    {this.renderAttendanceRows()}
                </tbody>
              </table>
            </div>
            <Button
              color="green">
              Confirm Attendance
            </Button>
          </form>

        </InnerView>
      );
    },
});
    



module.exports = ChairAttendanceView;
