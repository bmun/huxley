/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react');
var Router = require('react-router-component');

var AdvisorProfileView = require('./components/AdvisorProfileView');
var CurrentUserStore = require('./stores/CurrentUserStore');
var LoginView = require('./components/LoginView');
var RegistrationView = require('./components/RegistrationView');

var Locations = Router.Locations;
var Location = Router.Location;

var Huxley = React.createClass({
  mixins: [Router.NavigatableMixin],

  componentDidMount: function() {
    console.log(this.context.router);
    CurrentUserStore.addChangeListener(function() {
      if (!CurrentUserStore.isUserLoggedIn()) {
        this.navigate('/www/login');
      } else if (CurrentUserStore.isUserAdvisor()) {
        this.navigate('/www/advisor/profile');
      }
    }.bind(this));
  },

  render: function() {
    return (
      <Locations contextual>
        <Location path="/login" handler={LoginView} />
        <Location path="/register" handler={RegistrationView} />
        <Location path="/advisor/profile" handler={AdvisorProfileView} />
      </Locations>
    );
  }
});

module.exports = Huxley;
