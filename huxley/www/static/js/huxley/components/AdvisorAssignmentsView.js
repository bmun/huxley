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

var AssignmentStore = require('../stores/AssignmentStore');
var Button = require('./Button');
var CommitteeStore = require('../stores/CommitteeStore');
var ConferenceContext = require('./ConferenceContext');
var CountryStore = require('../stores/CountryStore');
var CurrentUserStore = require('../stores/CurrentUserStore');
var CurrentUserActions = require('../actions/CurrentUserActions');
var InnerView = require('./InnerView');

var AdvisorAssignmentsView = React.createClass({
  mixins: [
    Router.Navigation,
  ],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  getInitialState: function() {
    return {
      assignments: [],
      committees: {},
      countries: {},
      loading: false
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
    CommitteeStore.getCommittees(function(committees) {
      var new_committees = {};
      for (var i = 0; i < committees.length; i++) {
        new_committees[committees[i].id] = committees[i];
      }
      this.setState({committees: new_committees});
    }.bind(this));
    CountryStore.getCountries(function(countries) {
      var new_countries = {};
      for (var i = 0; i <countries.length; i++) {
        new_countries[countries[i].id] = countries[i];
      }
      this.setState({countries: new_countries})
    }.bind(this));
  },

  render: function() {
    var finalized = CurrentUserStore.getFinalized();
    var conference = this.context.conference;
    return (
      <InnerView>
        <h2>Assignments</h2>
        <p>
          Here you can view your tentative assignments for BMUN {conference.session}. If you
          would like to request more slots, please email <a href="mailto:info@bmun.org">
          info@bmun.org</a>. In the coming months
          we will ask that you finalize your assignment roster and input your
          delegates' names.
        </p>
        <form>
          <div className="tablemenu header" />
          <div className="table-container">
            <table className="table highlight-cells">
              <tbody>
                <tr>
                  <th>Committee</th>
                  <th>Country</th>
                  <th>Delegation Size</th>
                  <th>{finalized ?
                    "" :
                    "Delete Assignments"}
                  </th>
                </tr>
                {this.renderAssignmentRows()}
              </tbody>
            </table>
          </div>
          <div className="tablemenu footer" />
          {finalized ?
            <div> </div> :
            <Button
              color="green"
              size="large"
              onClick={this._handleFinalize}
              loading={this.state.loading}>
              Finalize Assignments
            </Button>}
        </form>
      </InnerView>
    );
  },

  renderAssignmentRows: function() {
    var committees = this.state.committees;
    var countries = this.state.countries;
    var finalized = CurrentUserStore.getFinalized();
    return this.state.assignments.map(function(assignment) {
      return (
        <tr>
          <td>{committees[assignment.committee].name}</td>
          <td>{countries[assignment.country].name}</td>
          <td>{committees[assignment.committee].delegation_size}</td>
          <td>{finalized ?
            <div/> :
            <Button color="red"
                    size="small"
                    onClick={this._handleAssignmentDelete.bind(this, assignment)}>
                    Delete Assignment
            </Button>}
          </td>
        </tr>
      )
    }.bind(this));
  },

  _handleFinalize: function(event) {
    var confirm = window.confirm("By pressing okay you are committing to the financial responsibility of each assingment. Are you sure you want to finalize assignments?");
    var school = CurrentUserStore.getCurrentUser().school;
    if (confirm) {
      this.setState({loading: true});
      $.ajax ({
        type: 'PUT',
        url: '/api/schools/'+school.id,
        data: {
          assignments_finalized: true,
        },
        success: this._handleFinalizedSuccess,
        error: this._handleError
      });
    }
  },

  _handleAssignmentDelete: function(assignment) {
    var confirm = window.confirm("Are you sure you want to delete this assignment");
    if (confirm) {
      this.setState({loading: true});
      $.ajax ({
        type: 'PUT',
        url: '/api/assignments/'+assignment.id,
        data: {
          rejected: true,
        },
        success: this._handleAssignmentDeleteSuccess,
        error: this._handleError,
      });
    }
  },

  _handleFinalizedSuccess: function(data, status, jqXHR) {
    CurrentUserActions.updateSchool(jqXHR.responseJSON);
    this.setState({loading: false});
    this.transitionTo('/advisor/assignments');
  },

  _handleAssignmentDeleteSuccess: function(data, status, jqXHR) {
    var assignments = this.state.assignments
    assignments = assignments.filter(function (assignment) {
      return assignment.id != jqXHR.responseJSON.id
    })
    this.setState({assignments: assignments})
    this.setState({loading: false});
    this.transitionTo('/advisor/assignments');
  },

  _handleError: function(jqXHR, status, error) {
    window.alert("Something went wrong. Please try again.");
    this.setState({loading: false});
  },

   _handleSuccess: function(event) {
    this.setState({loading: false});
    this.transitionTo('/advisor/assignments');
  }
});

module.exports = AdvisorAssignmentsView;
