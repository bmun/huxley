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
      generated: false
    };
  },

  render: function() {
    if (this.state.generated) {
      return (
        <Button
          color="green"
          size="small"
          onClick={this._generateInvoice}>
          Your Invoice Will Be Emailed Within 2 Business Days
        </Button>
      )
    }
    else {
      return (
        <Button
          color="green"
          size="small"
          onClick={this._generateInvoice}>
          Generate Your Invoice
        </Button>
      )
    };
  },

  _generateInvoice: function(event) {
    var user = this.props.user.getData();
    var school = this.props.user.getSchool();

    $.ajax({
      type: 'POST',
      url: '/api/schools/'+school.id+'/invoice/',
      success: this._handleSuccess,
      error: this._handleError,
      dataType: 'json'
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    this.setState({generated: true});
  },

  _handleError: function(jqXHR, status, error) {
    this.setState({generated: true});
  }

});

module.exports = InvoiceButton;
