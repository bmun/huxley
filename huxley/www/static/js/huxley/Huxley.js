/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

var React = require('react');
var Router = require('react-router-component');

var LoginView = require('./components/LoginView');
var RegistrationView = require('./components/RegistrationView');

var Locations = Router.Locations;
var Location = Router.Location;

var Huxley = React.createClass({
  render: function() {
    return (
      <Locations contextual>
        <Location path="/login" handler={LoginView} />
        <Location path="/register" handler={RegistrationView} />
      </Locations>
    );
  }
});

module.exports = Huxley;
