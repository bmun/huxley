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
      </InnerView>
    );
  },
});

module.exports = DelegateProfileView;
