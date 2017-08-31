/**
* Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

const React = require('react');
const ReactRouter = require('react-router');

const AssignmentStore = require('stores/AssignmentStore');
const ConferenceContext = require('components/ConferenceContext');
const CommitteeStore = require('stores/CommitteeStore');
const CountryStore = require('stores/CountryStore');
const CurrentUserStore = require('stores/CurrentUserStore');
const DelegateActions = require('actions/DelegateActions');
const DelegateStore = require('stores/DelegateStore');
const SchoolStore = require('stores/SchoolStore');
const InnerView = require('components/InnerView');
const TextTemplate = require('components/core/TextTemplate');
const User = require('utils/User');

require('css/Table.less');
const DelegateProfileViewText = require('text/DelegateProfileViewText.md');

const DelegateProfileView = React.createClass({
  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
  },

  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    var committees = CommitteeStore.getCommittees();
    var countries = CountryStore.getCountries();
    var delegate = DelegateStore.getDelegate(user.delegate);
    var assignment =
      delegate && AssignmentStore.getAssignment(delegate.assignment);
    var school = delegate && SchoolStore.getSchool(delegate.school);
    return {
      assignment: assignment,
      committees: committees,
      countries: countries,
      delegate: delegate,
      school: school,
    };
  },

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isDelegate(user)) {
      this.history.pushState(null, '/');
    }
  },

  componentDidMount() {
    var user = CurrentUserStore.getCurrentUser();
    this._assignmentToken = AssignmentStore.addListener(() => {
      var delegate = this.state.delegate;
      this.setState({
        assignment:
          delegate && AssignmentStore.getAssignment(delegate.assignment),
      });
    });

    this._committeesToken = CommitteeStore.addListener(() => {
      this.setState({committees: CommitteeStore.getCommittees()});
    });

    this._countriesToken = CountryStore.addListener(() => {
      this.setState({countries: CountryStore.getCountries()});
    });

    this._delegateToken = DelegateStore.addListener(() => {
      var delegate = DelegateStore.getDelegate(user.delegate);
      this.setState({
        delegate: delegate,
        assignment: AssignmentStore.getAssignment(delegate.assignment),
        school: SchoolStore.getSchool(delegate.school),
      });
    });

    this._schoolToken = SchoolStore.addListener(() => {
      var delegate = this.state.delegate;
      this.setState({
        school: delegate && SchoolStore.getSchool(delegate.school),
      });
    });
  },

  componentWillUnmount() {
    this._assignmentToken && this._assignmentToken.remove();
    this._committeesToken && this._committeesToken.remove();
    this._countriesToken && this._countriesToken.remove();
    this._delegateToken && this._delegateToken.remove();
    this._schoolToken && this._schoolToken.remove();
  },

  render() {
    var user = CurrentUserStore.getCurrentUser();
    var assignment = this.state.assignment;
    var committees = this.state.committees;
    var countries = this.state.countries;
    var delegate = this.state.delegate;
    var school = this.state.school;
    var text = <div />;

    if (
      assignment &&
      school &&
      Object.keys(committees).length &&
      Object.keys(countries).length
    ) {
      text = (
        <TextTemplate
          firstName={delegate.name}
          schoolName={school.name}
          conferenceSession={conference.session}
          committee={committees[assignment.committee].full_name}
          country={countries[assignment.country].name}>
          {DelegateProfileViewText}
        </TextTemplate>
      );
    }

    return (
      <InnerView>
        <div style={{textAlign: 'center'}}>
          <br />
          <h2>We are excited to have you at BMUN this year!</h2>
          <br />
        </div>
        {text}
        <h4>Below is your attendance from conference.</h4>
        <div className="table-container" style={{margin: '10px auto auto 0px'}}>
          <table>
            <thead>
              <tr>
                <th>Session</th>
                <th>Friday Evening</th>
                <th>Saturday Morning</th>
                <th>Saturday Afternoon</th>
                <th>Sunday Morning</th>
              </tr>
            </thead>
            {this.state.delegate ? this.renderAttendanceRow() : <tbody />}
          </table>
        </div>
      </InnerView>
    );
  },

  renderAttendanceRow: function() {
    var delegate = this.state.delegate;
    return (
      <tbody>
        <tr>
          <td>Attendance</td>
          <td>
            {delegate.session_one ? 'Attended' : ''}
          </td>
          <td>
            {delegate.session_two ? 'Attended' : ''}
          </td>
          <td>
            {delegate.session_three ? 'Attended' : ''}
          </td>
          <td>
            {delegate.session_four ? 'Attended' : ''}
          </td>
        </tr>
      </tbody>
    );
  },
});

module.exports = DelegateProfileView;
