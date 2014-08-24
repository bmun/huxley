/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var $ = require('jquery');
var React = require('react/addons');

var Button = require('./Button');

var ChangePasswordView = React.createClass({
  mixins: [React.addons.LinkedStateMixin],

  propTypes: {
	isVisible: React.PropTypes.bool.isRequired,
	onSuccess: React.PropTypes.func.isRequired
  },

  getInitialState: function() {
	return {
	  message: '',
	  success: false,
	  loading: false,
	  currentPassword: '',
	  newPassword: '',
	  newPassword2: '',
	};
  },

  componentWillReceiveProps: function(nextProps) {
	this.setState(this.getInitialState());
  },

  render: function() {
	if (!this.props.isVisible) {
	  return <div />;
	}

	return (
	  <div
		id="changepassword-container"
		className="change-password rounded-bottom transparent">
		<form
		  id="changepassword"
		  onSubmit={this._handleSubmit}>
		  <div className="input">
			<label htmlFor="oldpassword">Current Password</label>
			<input
			  type="password"
			  className="rounded-small"
			  valueLink={this.linkState('currentPassword')}
			/>
		  </div>
		  <div className="input">
			<label htmlFor="newpassword">New Password</label>
			<input
			  type="password"
			  className="rounded-small"
			  valueLink={this.linkState('newPassword')}
			/>
		  </div>
		  <div className="input">
			<label htmlFor="newpassword">New Password (again)</label>
			<input
			  type="password"
			  className="rounded-small"
			  valueLink={this.linkState('newPassword2')}
			/>
		  </div>
		  <div className="rounded-small topbarbutton">
			<Button
			  color="green"
			  size="small"
			  loading={this.state.loading}>
			  Change Password!
			</Button>
		  </div>
		</form>
		{this.renderMessage()}
	  </div>
	);
  },

  renderMessage: function() {
	if (!this.state.message) {
	  return null;
	}

	return (
	  <div id="message">
		<label className={this.state.success ? 'success' : 'error'}>
		  {this.state.message}
		</label>
	  </div>
	);
  },

  onSuccess: function() {
	setTimeout(this.props.onSuccess, 500);
  },

  _handleSubmit: function(event) {
	if (this.state.newPassword != this.state.newPassword2) {
	  this.setState({
		message: 'Please enter the same password again',
		success: false,
	  });
	} else {
	  this.setState({loading: true});
	  $.ajax({
		type: 'PUT',
		url: '/api/users/me/password',
		data: {
		  password: this.state.currentPassword,
		  new_password: this.state.newPassword,
		},
		success: this._handleSuccess,
		error: this._handleError
	  }),
	  event.preventDefault();
	}
  },

  _handleSuccess: function(data, status, jqXHR) {
	this.setState({
	  success: true,
	  message: 'Success',
	  currentPassword: '',
	  newPassword: '',
	  newPassword2: '',
	}, this.onSuccess);
  },

  _handleError: function(jqXHR, status, error) {
	var response = jqXHR.responseJSON;
	this.setState({
	  message: response.detail,
	  success: false,
	});
  },
});

module.exports = ChangePasswordView;
