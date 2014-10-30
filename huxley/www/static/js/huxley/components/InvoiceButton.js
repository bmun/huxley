/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var $ = require('jquery');
var React = require('react');

var Button = require('./Button');

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
          Your Invoice Has Been Generated
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

    // return (
    //     <Button
    //       color="green"
    //       size="small"
    //       onClick={this._generateInvoice}>
    //       Generate Your Invoice
    //     </Button>
    //   );

  },

  _generateInvoice: function(event) {
    var user = this.props.user.getData();
    var school = this.props.user.getSchool();

    $.ajax({
      type: 'POST',
      url: '/api/schools/'+school.id+'/invoice/',
      data: {
        'user.id': user.id,
        'user.name': user.name,
        'school.name': school.name,
        'school.fees_owed': school.fees_owed,
        'school.fees_paid': school.fees_paid
      },
      success: this._handleSuccess,
      error: this._handleError,
      dataType: 'json'
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    console.log("helloo");
    console.log(data);
    this.setState({generated: true});
  },

  _handleError: function(jqXHR, status, error) {
    console.log("error");
    var response = jqXHR.responseText;
    console.log(response);
  }

});

module.exports = InvoiceButton;
