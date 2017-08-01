/**
* Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var Button = require('components/core/Button');
var AssignmentStore = require('stores/AssignmentStore');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateActions = require('actions/DelegateActions');
var DelegationAttendanceRow = require('components/DelegationAttendanceRow');
var DelegateStore = require('stores/DelegateStore');
var InnerView = require('components/InnerView');
var TextTemplate = require('components/core/TextTemplate');
var User = require('utils/User');

require('css/Table.less');
var ChairAttendanceViewText = require('text/ChairAttendanceViewText.md');

var ChairAttendanceView = React.createClass({
  mixins: [ReactRouter.History],

  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    return {
      assignments: AssignmentStore.getCommitteeAssignments(user.committee),
      countries: CountryStore.getCountries(),
      country_assignments: {},
      delegates: DelegateStore.getCommitteeDelegates(user.committee),
      loading: false,
      success: false,
      attendance: {},
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
    var delegates = this.state.delegates;
    var attendance = this.state.attendance;
    var update = {};
    for (var delegate of delegates) {
      var delegateAttendance = [];
      delegateAttendance[0] = delegate.voting;
      delegateAttendance[1] = delegate.session_one;
      delegateAttendance[2] = delegate.session_two;
      delegateAttendance[3] = delegate.session_three;
      delegateAttendance[4] = delegate.session_four;
      update[delegate.assignment] = delegateAttendance;
    }
    this.setState({attendance: Object.assign({}, attendance, update)});

    this._delegatesToken = DelegateStore.addListener(() => {
      var delegates =  DelegateStore.getCommitteeDelegates(user.committee);
      var update = {};
      for (var delegate of delegates) {
        var delegateAttendance = [];
        delegateAttendance[0] = delegate.voting;
        delegateAttendance[1] = delegate.session_one;
        delegateAttendance[2] = delegate.session_two;
        delegateAttendance[3] = delegate.session_three;
        delegateAttendance[4] = delegate.session_four;
        update[delegate.assignment] = delegateAttendance;
      }
      this.setState({
        delegates: delegates,
        attendance: Object.assign({}, attendance, update),
      });
    });

    this._assignmentsToken = AssignmentStore.addListener(() => {
      var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
      var countries = this.state.countries;
      if (Object.keys(countries).length) {
        assignments.sort((a1, a2) => countries[a1.country].name < countries[a2.country].name ? -1 : 1);
      }
      this.setState({assignments: assignments});
    });

    this._countriesToken = CountryStore.addListener(() => {
      var assignments = this.state.assignments;
      var countries = CountryStore.getCountries();
      if (assignments.length) {
        assignments.sort((a1, a2) => countries[a1.country].name < countries[a2.country].name ? -1 : 1);
      }
      this.setState({
        assignments: assignments,
        countries: countries
      });
    });
  },

  componentWillUnmount() {
    this._successTimout && clearTimeout(this._successTimeout);
    this._countriesToken && this._countriesToken.remove();
    this._delegatesToken && this._delegatesToken.remove();
    this._assignmentsToken && this._assignmentsToken.remove();
  },

  render() {
    return (
      <InnerView>
        <TextTemplate>
          {ChairAttendanceViewText}
        </TextTemplate>
        <form>
          <div className="table-container">
            <table style={{margin: '10px auto 0px auto', tableLayout: 'fixed'}}>
              <thead>
                <tr>
                  <th>Assignment</th>
                  <th>Voting</th>
                  <th>Session One</th>
                  <th>Session Two</th>
                  <th>Session Three</th>
                  <th>Session Four</th>
                </tr>
              </thead>
            </table>
            <div style={{overflowY: 'auto', maxHeight: '50vh'}}>
              <table
                className="table highlight-cells"
                style={{margin: '0px auto 20px auto', tableLayout: 'fixed'}}>
                <tbody>
                  {this.renderAttendanceRows()}
                </tbody>
              </table>
            </div>
          </div>
          <Button
            color="green"
            onClick={this._handleSaveAttendance}
            loading={this.state.loading}
            success={this.state.success}>
            Save Attendance
          </Button>
        </form>
      </InnerView>
    );
  },

  renderAttendanceRows() {
    var assignments = this.state.assignments;
    var attendance = this.state.attendance;
    var assignmentIDs = Object.keys(attendance);
    var countries = this.state.countries;
    assignments = assignments.filter(a => assignmentIDs.indexOf(""+a.id) > -1);
    return assignments.map(assignment => 
      <DelegationAttendanceRow
        key={assignment.id}
        onChange={this._handleAttendanceChange}
        countryName={
          Object.keys(countries).length ? countries[assignment.country].name : ""+assignment.country
        }
        assignmentID={assignment.id}
        attendance={attendance[assignment.id]}
      />
    );
  },

  _handleAttendanceChange(field, assignmentID, event) {
    var attendanceMap = this.state.attendance;
    var oldAttendance = attendanceMap[assignmentID];
    var newAttendance = [... oldAttendance];
    newAttendance[field] = !newAttendance[field];
    var update = {};
    update[assignmentID] = newAttendance;
    this.setState({attendance: Object.assign({}, attendanceMap, update)});
  },

  _handleSaveAttendance(event) {
    this._successTimout && clearTimeout(this._successTimeout);
    this.setState({loading: true});
    var committee = CurrentUserStore.getCurrentUser().committee;
    var attendanceMap = this.state.attendance;
    var delegates = this.state.delegates;
    var toSave = [];
    for (var delegate of delegates) {
      var attendance = attendanceMap[delegate.assignment];
      if (delegate.attendance != attendance) {
        var update = {voting: attendance[0],
                      session_one: attendance[1],
                      session_two: attendance[2],
                      session_three: attendance[3],
                      session_four: attendance[4]};
        toSave.push(Object.assign({}, delegate, update))
      }
    }
    DelegateActions.updateCommitteeDelegates(committee, toSave, this._handleSuccess, this._handleError);
    event.preventDefault();
  },

  _handleSuccess: function(response) {
    this.setState({
      loading: false,
      success: true,
    });

    this._successTimeout = setTimeout(
      () => this.setState({success: false}),
      2000,
    );
  },

  _handleError: function(response) {
    this.setState({loading: false});
    window.alert(
      'Something went wrong. Please refresh your page and try again.',
    );
  },
});

module.exports = ChairAttendanceView;
