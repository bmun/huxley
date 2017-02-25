/**
* Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var Button = require('components/Button');
var AssignmentStore = require('stores/AssignmentStore');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateActions = require('actions/DelegateActions');
var DelegationAttendanceRow = require('components/DelegationAttendanceRow');
var DelegateStore = require('stores/DelegateStore');
var InnerView = require('components/InnerView');
var User = require('utils/User');

var ChairAttendanceView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    return {
      assignments: AssignmentStore.getCommitteeAssignments(user.committee),
      countries: CountryStore.getCountries(),
      country_assignments: {},
      delegates: DelegateStore.getCommitteeDelegates(user.committee),
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
    this._mapAssignments();
    this._delegatesToken = DelegateStore.addListener(() => {
      this.setState({delegates: DelegateStore.getCommitteeDelegates(user.committee)});
      this._mapAssignments();
    });

    this._assignmentsToken = AssignmentStore.addListener(() => {
      this.setState({assignments: AssignmentStore.getCommitteeAssignments(user.committee)});
      this._mapAssignments();
    });

    this._countriesToken = CountryStore.addListener(() => {
      this.setState({countries: CountryStore.getCountries()});
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
        <h2>Attendance</h2>
        <p>
          Here you can take attendance for delegates. Note that confirming 
          attendance will alert the advisor as to if their delegates have 
          shown up to committee.
        </p>
        <p>
          <strong>
            Only one chair at a time should be logged in. Changes may be lost 
            otherwise.
          </strong>
        </p>
        <form>
          <div className="table-container" style={{'overflowY': 'auto', 'maxHeight': '50vh'}}>
            <table className="table highlight-cells">
              <thead>
                <tr>
                  <th>Assignment</th>
                  <th>Session One</th>
                  <th>Session Two</th>
                  <th>Session Three</th>
                  <th>Session Four</th>
                </tr>
              </thead>
              <tbody>
                {this.renderAttendanceRows()}
              </tbody>
            </table>
          </div>
          <Button
            color="green"
            onClick={this._handleSaveAttendance}>
            Confirm Attendance
          </Button>
        </form>
      </InnerView>
    );
  },

  renderAttendanceRows() {
    var committeeCountryIDs = Object.keys(this.state.country_assignments);
    var countries = this.state.countries;
    if (Object.keys(countries).length){
      committeeCountryIDs.sort((c1, c2) => countries[c1].name < countries[c2].name ? -1 : 1);
    }
    return committeeCountryIDs.map(country => 
      <DelegationAttendanceRow
        key={country}
        onChange={this._handleAttendanceChange}
        countryName={Object.keys(countries).length ? countries[country].name : country}
        countryID={country}
        delegates={this.state.country_assignments[country]}
      />
    );
  },

  _mapAssignments() {
    var user = CurrentUserStore.getCurrentUser();
    var country_assignments = {};
    var delegates = this.state.delegates;
    var assignments = this.state.assignments;
    for (var delegate of delegates) {
      var assignment = assignments.find(assignment => assignment.id == delegate.assignment);
      if (!assignment) continue;
      var countryID = assignment.country;
      if (countryID in country_assignments) {
        country_assignments[countryID].push(delegate);
      } else {
        country_assignments[countryID] = [delegate];
      }
    }
    
    this.setState({country_assignments: country_assignments});
  }, 

  _handleAttendanceChange(session, country, event) {
    var country_assignments = this.state.country_assignments;
    var country_delegates = country_assignments[country];
    for (var delegate of country_delegates) {
      delegate[session] = !delegate[session];
    }

    this.setState({country_assignments: country_assignments});
  },

  _handleSaveAttendance(event) {
    var committee = CurrentUserStore.getCurrentUser().committee;
    var country_assignments = this.state.country_assignments;
    var delegates = [];
    for (var country in country_assignments) {
      delegates = delegates.concat(country_assignments[country]);
    }
    DelegateActions.updateCommitteeDelegates(committee, delegates);
    event.preventDefault();
  },

});
    
module.exports = ChairAttendanceView;
