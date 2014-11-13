/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var $ = require('jquery');
var Button = require('./Button');
var React = require('react');

var InvoiceButton = React.createClass({
  getInitialState: function() {
    return {
      loading: false,
      generated: false,
      unauthorized: false
    };
  },

  render: function() {
    var buttonText = 'Generate Your Invoice';
    if (this.state.generated) {
      buttonText = 'Your Invoice Will Be Emailed Within 2 Business Days';
    }
    if (this.state.unauthorized) {
      buttonText = 'Something Went Wrong - Please Email treasurer@bmun.org';
    }
    return (
      <Button
        color="green"
        size="small"
        loading={this.state.loading}
        onClick={this.state.generated 
          ? null
          : this._handleClick}>
        {buttonText}
      </Button>
    )
  },

  _handleClick: function(event) {
    this.setState({loading: true});
    var user = this.props.user.getData();
    var school = this.props.user.getSchool();
    $.ajax({
      type: 'POST',
      url: '/api/schools/' + school.id + '/invoice/',
      success: this._handleSuccess,
      error: this._handleError,
      dataType: 'json'
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    this.setState({generated: true});
    this.setState({loading: false});
  },

  _handleError: function(jqXHR, status, error) {
    // Unrelated errors might still pop up even though invoices are being created
    if (jqXHR.status == 201) {
      this.setState({generated: true});
    } else {
      this.setState({unauthorized: true});
    }
    this.setState({loading: false});
  }

});

module.exports = InvoiceButton;
