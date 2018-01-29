/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

'use strict';

const React = require('react');
const ReactRouter = require('react-router');

const Button = require('components/core/Button');
const ConferenceContext = require('components/ConferenceContext');
const CurrentUserStore = require('stores/CurrentUserStore');
const InnerView = require('components/InnerView');
const TextTemplate = require('components/core/TextTemplate');
const User = require('utils/User');

const ServerAPI = require('lib/ServerAPI');

require('css/Table.less');
const DelegateProfileViewText = require('text/DelegateProfileViewText.md');

const DelegateProfileView = React.createClass({
  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
  },

  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    var delegate = user.delegate;
    return {
      delegate: delegate,
    };
  },

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isDelegate(user)) {
      this.history.pushState(null, '/');
    }
  },

  render() {
    var user = CurrentUserStore.getCurrentUser();
    var delegate = this.state.delegate;
    var assignment = delegate && delegate.assignment;
    var committee = delegate && delegate.assignment.committee;
    var country = delegate && delegate.assignment.country;
    var school = delegate && delegate.school;
    var text = <div />;

    if (assignment && school && committee && country) {
      text = (
        <TextTemplate
          firstName={delegate.name}
          schoolName={school.name}
          conferenceSession={conference.session}
          committee={committee.full_name}
          country={country.name}>
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
          <td>{delegate.session_one ? 'Attended' : ''}</td>
          <td>{delegate.session_two ? 'Attended' : ''}</td>
          <td>{delegate.session_three ? 'Attended' : ''}</td>
          <td>{delegate.session_four ? 'Attended' : ''}</td>
        </tr>
      </tbody>
    );
  },
});

module.exports = DelegateProfileView;
