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
  mixins: [
    ReactRouter.History,
  ],

  render: function() {
    if (User.isChair(this.props.user)) {
      return (
        <InnerView>
          <h2>Chair View</h2>
          <p>
            Here you can view your tentative assignments for BMUN {conference.session}. If you
            would like to request more slots, please email <a href="mailto:info@bmun.org">
            info@bmun.org</a>. The assignment finalization deadline is January 23rd.
            After assignment finalization we will ask that you assign the
            delegates you have added in the delegates tab to the assignments
            given to you.
          </p>
        </InnerView>
      );
    } else {
      return (
        <PermissionDeniedView />
      );
    }
  },
});

module.exports = ChairAttendanceView;
