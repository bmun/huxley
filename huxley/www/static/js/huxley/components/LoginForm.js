/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

var console = require('console');

var $ = require('jquery');
var Link = require('react-router-component').Link;
var React = require('react/addons');

var OuterView = require('./OuterView');

require('jquery-ui/effect-shake');


var LoginForm = React.createClass({
  mixins: [React.addons.LinkedStateMixin],

  getInitialState: function() {
    return {
      error: null,
      username: null,
      password: null,
      loading: false
    };
  },

  render: function() {
    var cx = React.addons.classSet;
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
            <button
              className={cx({
                'button': true,
                'button-blue': true,
                'login-button': true,
                'rounded-small': true,
                'loading': this.state.loading
              })}
              type="submit">
              <span>Log In</span>
            </button>
            <Link
              className="js-nav button button-green rounded-small"
              href="/www/register">
              Register for BMUN
            </Link>
          </div>
          <a className="js-nav" href="#">
            Forgot your password?
          </a>
          {this.renderError()}
        </form>
      </OuterView>
    );
  },

  renderHeader: function() {
    return (
      <div className="logo">
        <hr />
        <h1>Welcome to Huxley</h1>
        <span className="help-text">for Berkeley Model United Nations</span>
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
    console.log(jqXHR.responseText);
    this.setState({
      error: null,
      loading: false
    });
  },

  _handleError: function(jqXHR, status, error) {
    response = jqXHR.responseJSON;
    if (!response.detail) {
      return;
    }

    this.setState({
      error: response.detail,
      loading: false
    }, function() {
      $(this.getDOMNode()).effect(
        'shake',
        {direction: 'up', times: 2, distance: 2},
        250
      );
    }.bind(this));
  }
});

module.exports = LoginForm;
