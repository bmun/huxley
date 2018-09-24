/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

'use strict';

const React = require('react');
const ReactRouter = require('react-router');

const ConferenceContext = require('components/ConferenceContext');
const CurrentUserStore = require('stores/CurrentUserStore');
const InnerView = require('components/InnerView');
const TextTemplate = require('components/core/TextTemplate');
const User = require('utils/User');

require('css/Table.less');
const DelegateProfileViewText = require('text/DelegateProfileViewText.md');

const DelegateChecklistPositionPaperText = require('text/checklists/DelegateChecklistPositionPaperText.md');
const DelegateChecklistWaiverText = require('text/checklists/DelegateChecklistWaiverText.md');

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
    var summary = <div />;
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

    var positionPaperCheck = '';
    if (assignment && assignment.paper && assignment.paper.file) {
      positionPaperCheck = '\u2611';
    } else {
      positionPaperCheck = '\u2610';
    }

    var waiverCheck = '';
    if (delegate && delegate.waiver_submitted) {
      waiverCheck = '\u2611';
    } else {
      waiverCheck = '\u2610';
    }

    var checklist = (
      <table>
        <thead>
          <tr>
            <th>Delegate Checklist</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              {positionPaperCheck} <b>Turn in Position Paper</b>
              <br />
              <TextTemplate>{DelegateChecklistPositionPaperText}</TextTemplate>
            </td>
          </tr>
          <tr>
            <td>
              {waiverCheck} <b>Turn in Waiver Form</b>
              <br />
              <TextTemplate>{DelegateChecklistWaiverText}</TextTemplate>
            </td>
          </tr>
        </tbody>
      </table>
    );

    if (delegate.published_summary) {
      summary = (
        <table>
          <thead>
            <tr>
              <th>Feedback From Your Chairs:</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{delegate.published_summary}</td>
            </tr>
          </tbody>
        </table>
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
        <br />
        {checklist}
        {summary}
      </InnerView>
    );
  },
});

module.exports = DelegateProfileView;
