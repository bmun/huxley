/**
* Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
*
* @jsx React.DOM
+*/

'use strict';

var $ = require('jquery');
var React = require('react');
var Router = require('react-router');
var Modal = require('react-modal');

var AssignmentStore = require('../stores/AssignmentStore');
var Button = require('./Button');
var CommitteeStore = require('../stores/CommitteeStore');
var CountryStore = require('../stores/CountryStore');
var CurrentUserStore = require('../stores/CurrentUserStore');
var DelegateStore = require('../stores/DelegateStore');
var CurrentUserActions = require('../actions/CurrentUserActions');
var InnerView = require('./InnerView');

var AdvisorRosterView = React.createClass({
  mixins: [
    Router.Navigation,
  ],

  getInitialState: function() {
    return {
      assignments: [],
      delegates: [],
    };
  },

  componentWillMount: function() {
    var user = CurrentUserStore.getCurrentUser();
    AssignmentStore.getAssignments(user.school.id, function(assignments) {
      this.setState({assignments: assignments.filter(
        function(assignment) {
          return !assignment.rejected
        }
      )});
    }.bind(this));
    DelegateStore.getDelegates(user.school.id, function(delegates) {
      this.setState({delegates: delegates});
    }.bind(this));
  },

  render: function() {
    return (
      <InnerView>
        <h2>Roster</h2>
        <p>
          Here you can add your schools delegates to your roster.
          Any comments that chairs have about your delegate will appear here.
        </p>
        <form>
          <div className="tablemenu header" />
          <div className="table-container">
            <table className="table highlight-cells">
              <tr>
                <th>Delegate</th>
                <th>Email</th>
                <th>Summary</th>
              </tr>
              {this.renderRosterRows()}
              {this._handleAddDelegate()}
            </table>
          </div>
        </form>
        <div>
          <Button onClick={this._handleAddDelegate}>Add Delegate</Button>
        </div>
      </InnerView>
    );
  },

  renderRosterRows: function() {
    var committees = this.state.committees;
    var countries = this.state.countries;
    console.dir(this.state.delegates[0])
    return this.state.delegates.map(function(delegate) {
      return (
        <tr>
          <td>{delegate.name}</td>
          <td>{delegate.email}</td>
          <td>{delegate.summary}</td>
          <td>
            <Button>Delete</Button>
          </td>
        </tr>
      )
    }.bind(this));
  },

  _handleAddDelegate: function() {
    return (
      <form>
        <br>Name: <input type="text" placeholder="Name" valueLink={this.linkState('name')} /></br>
        <br>Email: <input type="text" placeholder="Email" valueLink={this.linkState('email')}/></br>
        <input type="submit" value="Submit" onclick={this._handleSubmit} />
      </form>
    )
  },

  _handleSubmit: function(data) {
    this.setState({loading: true});
    $.ajax({
      type: 'POST',
      url: '/api/delegate',
      data: {
        name: this.state.name,
        email: this.state.email,
      },
      success: this._handleSuccess,
      error: this._handleError,
      dataType: 'json'
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    console.log("success!");
  },

  _handleError: function(jqXHR, status, error) {
    var response = jqXHR.responseJSON;
    if (!response) {
      return;
    }

    this.setState({
      errors: response,
      loading: false
    }.bind(this));
  }

});

module.exports = AdvisorRosterView;
