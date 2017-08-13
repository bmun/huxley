/**
* Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

const React = require('react');
const ReactRouter = require('react-router');

const Button = require('components/core/Button');
const AssignmentStore = require('stores/AssignmentStore');
const ConferenceContext = require('components/ConferenceContext');
const CommitteeStore = require('stores/CommitteeStore');
const CountryStore = require('stores/CountryStore');
const CurrentUserStore = require('stores/CurrentUserStore');
const DelegateActions = require('actions/DelegateActions');
const DelegateStore = require('stores/DelegateStore');
// const SchoolStore = require('stores/SchoolStore');
const InnerView = require('components/InnerView');
const TextTemplate = require('components/core/TextTemplate');
const User = require('utils/User');

require('css/Table.less');
const DelegateProfileViewText = require('text/DelegateProfileViewText.md')

const DelegateProfileView = React.createClass({
  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
  },

  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    var delegate = user.delegate;
    var assignment = AssignmentStore.getAssignment(delegate.assignment);
    // var school = SchoolStore.getSchool(delegate.school);
    return {
      delegate: delegate,
      assignment: assignment,
      // school: school,
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
    var delegate = user.delegate;
    this._assignmentToken = AssignmentStore.addListener(() => {
      this.setState({
        assignment: AssignmentStore.getAssignment(delegate.assignment)
      });
    });

    // this._schoolToken = SchoolStore.addListener(() => {
    //   this.setState({school: SchoolStore.getSchool(delegate.school)})
    // })
  },

  componentWillUnmount() {
    this._assignmentToken && this._assignmentToken.remove();
  },

  render() {
    var user = CurrentUserStore.getCurrentUser();
    return (
      <InnerView>
        <TextTemplate
          firstName={user.first_name}
          schoolName='HHS'//{school.name}
          conferenceSession={conference.session}>
          {DelegateProfileViewText}
        </TextTemplate>
        <form>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Session</th>
                  <th>Attendance</th>
                </tr>
              </thead>
                {this.state.delegate ? this.renderAttendanceRows() : <tbody />}
            </table>
          </div>
        </form>
      </InnerView>
    );
  },

  renderAttendanceRows: function() {
    var delegate = this.state.delegate;
    return (
      <tbody>
        <tr>
          <td>
            Session One
          </td>
          <td>
            {delegate.session_one ? "Attended" : "Did not attend"}
          </td>
        </tr>
        <tr>
          <td>
            Session Two
          </td>
          <td>
            {delegate.session_two ? "Attended" : "Did not attend"}
          </td>
        </tr>
        <tr>
          <td>
            Session Three
          </td>
          <td>
            {delegate.session_three ? "Attended" : "Did not attend"}
          </td>
        </tr>
        <tr>
          <td>
            Session Four
          </td>
          <td>
            {delegate.session_four ? "Attended" : "Did not attend"}
          </td>
        </tr>
      </tbody>
    );
  },

});

module.exports = DelegateProfileView;