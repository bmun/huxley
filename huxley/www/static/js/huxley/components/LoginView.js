/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var console = require('console');

var $ = require('jquery');
var classNames = require('classnames');
var LinkedStateMixin = require('react-addons-linked-state-mixin');
var React = require('react');
var Router = require('react-router');


var Button = require('./Button');
var ConferenceContext = require('./ConferenceContext');
var CurrentUserActions = require('../actions/CurrentUserActions');
var NavLink = require('./NavLink');
var OuterView = require('./OuterView');
var User = require('../utils/User');

require('jquery-ui/effect-shake');

var LoginView = React.createClass({
  mixins: [
    LinkedStateMixin,
    Router.Navigation,
  ],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  getInitialState: function() {
    return {
      error: null,
      username: null,
      password: null,
      loading: false
    };
  },

  componentWillMount: function() {
    var {user} = this.props;
    if (User.isAnonymous(user)) {
      return;
    }
    if (User.isAdvisor(user)) {
      this.transitionTo('/advisor/profile');
    }
  },

  render: function() {
    return (
      <OuterView header={this.renderHeader()}>
        <form
          id="login"
          className="login-form"
          onSubmit={this._handleSubmit}>
          <div className="login-fields">
            <input
              className="text"
              type="text"
              name="username"
              placeholder="Username"
              valueLink={this.linkState('username')}
            />
            <input
              className="text"
              type="password"
              name="password"
              placeholder="Password"
              valueLink={this.linkState('password')}
            />
          </div>
          <div className="login-register">
            <Button
              color="blue"
              loading={this.state.loading}
              type="submit">
              Log In
            </Button>
            <Button color="green" href="/register">
              Register for BMUN
            </Button>
          </div>
          <NavLink direction="left" href="/password">
            Forgot your password?
          </NavLink>
          {this.renderError()}
        </form>
      </OuterView>
    );
  },

  renderHeader: function() {
    var conference = this.context.conference;
    return (
      <div className="logo">
        <hr />
        <h1>Welcome to Huxley</h1>
        <span className="help-text">for Berkeley Model United Nations</span>
        <br />
        <span className="help-text">a High School Conference</span>
        <br />
        <span className="help-text">
          {conference.start_date['month']} {conference.start_date['day']} -&nbsp;
          {conference.end_date['day']}, {conference.start_date['year']}
        </span>
      </div>
    );
  },

  renderError: function() {
    if (this.state.error) {
      return (
        <div id="errorcontainer">
          <label className="error">{this.state.error}</label>
        </div>
      );
    }

    return null;
  },

  _handleSubmit: function(event) {
    this.setState({loading: true});
    $.ajax({
      type: 'POST',
      url: '/api/users/me',
      data: {
        username: this.state.username,
        password: this.state.password
      },
      success: this._handleSuccess,
      error: this._handleError,
      dataType: 'json'
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    CurrentUserActions.login(jqXHR.responseJSON);
  },

  _handleError: function(jqXHR, status, error) {
    var response = jqXHR.responseJSON;
    if (!response.detail) {
      return;
    }

    this.setState({
      error: response.detail,
      loading: false
    }, function() {
      $('#huxley-app').effect(
        'shake',
        {direction: 'up', times: 2, distance: 2},
        250
      );
    }.bind(this));
  }
});

module.exports = LoginView;
