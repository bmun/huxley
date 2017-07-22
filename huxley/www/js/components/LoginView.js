/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var cx = require('classnames');
var React = require('react');
var ReactRouter = require('react-router');

var Button = require('components/core/Button');
var ConferenceContext = require('components/ConferenceContext');
var CurrentUserActions = require('actions/CurrentUserActions');
var NavLink = require('components/NavLink');
var OuterView = require('components/OuterView');
var ServerAPI = require('lib/ServerAPI');
var StatusLabel = require('components/core/StatusLabel');
var TextInput = require('components/core/TextInput');
var TextTemplate = require('components/core/TextTemplate');
var User = require('utils/User');

require('css/LoginForm.less');
var LoginViewText = require('text/LoginViewText.md');

var LoginView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
    shake: React.PropTypes.func,
  },

  getInitialState: function() {
    return {
      error: null,
      username: '',
      password: '',
      loading: false
    };
  },

  componentWillMount: function() {
    var {user} = this.props;
    if (User.isAnonymous(user)) {
      return;
    }
    if (User.isAdvisor(user)) {
      this.history.pushState(null, '/advisor/profile');
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
            <TextInput
              name="username"
              placeholder="Username"
              value={this.state.username}
              onChange={this._handleUsernameChange}
            />
            <TextInput
              type="password"
              name="password"
              placeholder="Password"
              value={this.state.password}
              onChange={this._handlePasswordChange}
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
        <TextTemplate
          conferenceStartMonth={conference.start_date['month']}
          conferenceStartDay={conference.start_date['day']}
          conferenceEndDay={conference.end_date['day']}
          conferenceStartYear={conference.start_date['year']}>
          {LoginViewText}
        </TextTemplate>
      </div>
    );
  },

  renderError: function() {
    if (this.state.error) {
      return (
        <StatusLabel status="error">{this.state.error}</StatusLabel>
      );
    }

    return null;
  },

  _handlePasswordChange: function(password) {
    this.setState({password});
  },

  _handleUsernameChange: function(username) {
    this.setState({username});
  },

  _handleSubmit: function(event) {
    this.setState({loading: true});
    ServerAPI.login(this.state.username, this.state.password)
      .then(this._handleSuccess, this._handleError);
    event.preventDefault();
  },

  _handleSuccess: function(responseJSON) {
    CurrentUserActions.login(responseJSON);
  },

  _handleError: function(responseJSON) {
    if (!responseJSON.detail) {
      return;
    }

    this.setState({
      error: responseJSON.detail,
      loading: false,
    }, () => {
      this.context.shake && this.context.shake();
    });
  }
});

module.exports = LoginView;
