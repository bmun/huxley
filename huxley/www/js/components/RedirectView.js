/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var OuterView = require('components/OuterView');
var User = require('utils/User');

var RedirectView = React.createClass({
  mixins: [ReactRouter.History],

  // componentDidMount: function() {
  //   var {user} = this.props;
  //   if (User.isAnonymous(user)) {
  //     this.history.pushState(null, '/login');
  //   } else if (User.isAdvisor(user)) {
  //     this.history.pushState(null, '/advisor/profile');
  //   } else if (User.isChair(user)) {
  //     this.history.pushState(null, '/chair/attendance');
  //   } else if (User.isDelegate(user)) {
  //     this.history.pushState(null, '/delegate/profile');
  //   }
  // },

  render: function() {
    // TODO: make this the same component as the loading indicator... when the
    // loading indicator is actually built.
    return <OuterView>Huxley is currently down for maintenance. You will be able to 
    register or acceess your account by 4:30pm PST on January 6th 2021. On behalf of Berkeley Model
    United Nations, we apologize for the inconvenience. 
    <br></br>
    <br/>Should you have an urgent matter to resolve, please contact info@bmun.org or tech@bmun.org</OuterView>;
  },
});

module.exports = RedirectView;
