/**
* Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var AssignmentStore = require('stores/AssignmentStore');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateStore = require('stores/DelegateStore');
var InnerView = require('components/InnerView');
var TextTemplate = require('components/core/TextTemplate');
var User = require('utils/User');

require('css/Table.less');
var ChairDelegateEmailViewText = require('text/ChairDelegateEmailViewText.md');

var ChairDelegateEmailView = React.createClass({
  mixins: [ReactRouter.History],

  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
    var countries = CountryStore.getCountries();
    var delegates = DelegateStore.getCommitteeDelegates(user.committee);

    if (assignments.length && Object.keys(countries).length) {
      assignments.sort(
        (a1, a2) =>
          countries[a1.country].name < countries[a2.country].name ? -1 : 1,
      );
    }

    return {
      assignments: assignments,
      countries: countries,
      delegates: delegates,
    };
  },

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isChair(user)) {
      this.history.pushState(null, '/');
    }
  },

  componentDidMount() {
    var user = CurrentUserStore.getCurrentUser();

    this._delegatesToken = DelegateStore.addListener(() => {
      var delegates = DelegateStore.getCommitteeDelegates(user.committee);
      this.setState({delegates: delegates});
    });

    this._assignmentsToken = AssignmentStore.addListener(() => {
      var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
      var countries = this.state.countries;
      if (Object.keys(countries).length) {
        assignments.sort(
          (a1, a2) =>
            countries[a1.country].name < countries[a2.country].name ? -1 : 1,
        );
      }
      this.setState({assignments: assignments});
    });

    this._countriesToken = CountryStore.addListener(() => {
      var assignments = this.state.assignments;
      var countries = CountryStore.getCountries();
      if (assignments.length) {
        assignments.sort(
          (a1, a2) =>
            countries[a1.country].name < countries[a2.country].name ? -1 : 1,
        );
      }
      this.setState({
        assignments: assignments,
        countries: countries,
      });
    });
  },

  componentWillUnmount() {
    this._countriesToken && this._countriesToken.remove();
    this._delegatesToken && this._delegatesToken.remove();
    this._assignmentsToken && this._assignmentsToken.remove();
  },

  render() {
    return (
      <InnerView>
        <TextTemplate>
          {ChairDelegateEmailViewText}
        </TextTemplate>
        <form>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Assignment</th>
                  <th>Email</th>
                </tr>
              </thead>
            </table>
            <div>
              <table
                className="table highlight-cells">
                <tbody>
                  {Object.keys(this.state.countries).length > 0
                    ? this.renderEmailRows()
                    : <tr />}
                </tbody>
              </table>
            </div>
          </div>
        </form>
      </InnerView>
    );
  },

  renderEmailRows() {
    var assignments = this.state.assignments;
    var delegates = this.state.delegates;
    var countries = this.state.countries;
    return delegates.map(delegate => {
      return (
        <tr key={delegate.id}>
          <td>
            {countries[assignments.find(a => a.id == delegate.assignment).country].name}
          </td>
          <td>
            {delegate.email}
          </td>
        </tr>
      );
    });
  },
});

module.exports = ChairDelegateEmailView;
