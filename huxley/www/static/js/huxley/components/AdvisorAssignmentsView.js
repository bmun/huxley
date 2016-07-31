/**
* Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var $ = require('jquery');
var React = require('react');
var ReactRouter = require('react-router');

var AssignmentStore = require('../stores/AssignmentStore');
var Button = require('./Button');
var CommitteeStore = require('../stores/CommitteeStore');
var ConferenceContext = require('./ConferenceContext');
var CountryStore = require('../stores/CountryStore');
var CurrentUserStore = require('../stores/CurrentUserStore');
var CurrentUserActions = require('../actions/CurrentUserActions');
var DelegateSelect = require('./DelegateSelect');
var DelegateStore = require('../stores/DelegateStore');
var InnerView = require('./InnerView');

var AdvisorAssignmentsView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  getInitialState: function() {
    return {
      assigned: {},
      assignments: [],
      committees: {},
      countries: {},
      delegates: [],
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
      for (var i = 0; i < countries.length; i++) {
        new_countries[countries[i].id] = countries[i];
      }
      this.setState({countries: new_countries})
    }.bind(this));
    DelegateStore.getDelegates(user.school.id, function(delegates) {
      // assigned is to manage the relation between an assignment and its delegates.
      var assigned = {};
      for (var i = 0; i < delegates.length; i++) {
        if (delegates[i].assignment) {
          if (delegates[i].assignment in assigned) {
            assigned[delegates[i].assignment][1] = delegates[i].id;
          } else {
            // We assume each assignment has at most two delegates assigned to it.
            // Single delegate assignments simply won't access the second slot.
            var slots = new Array(2).fill(0);
            slots[0] = delegates[i].id;
            assigned[delegates[i].assignment] = slots;
          }
        }
      }

      this.setState({
        delegates: delegates,
        assigned: assigned
      });
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
          <div className="table-container">
            <table className="table highlight-cells">
              <thead>
                <tr>
                  <th>Committee</th>
                  <th>Country</th>
                  <th>Delegation Size</th>
                  <th>{finalized ?
                    "Delegate" :
                    "Delete Assignments"}
                  </th>
                  <th>{finalized ?
                    "Delegate" :
                    ""}
                  </th>
                </tr>
              </thead>
              <tbody>
                {this.renderAssignmentRows()}
              </tbody>
            </table>
          </div>
          {finalized ?
            <Button
              color="green"
              size="large"
              onClick={this._handleSave}
              loading={this.state.loading}>
              Save
            </Button> :
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
            this.renderDelegateDropdown(assignment, 0) :
            <Button color="red"
                    size="small"
                    onClick={this._handleAssignmentDelete.bind(this, assignment)}>
                    Delete Assignment
            </Button>}
          </td>
          <td>{finalized && committees[assignment.committee].delegation_size == 2 ?
            this.renderDelegateDropdown(assignment, 1) :
            <div/>}
          </td>
        </tr>
      )
    }.bind(this));
  },

  renderDelegateDropdown: function(assignment, slot) {
    var selectedDelegateId = assignment.id in this.state.assigned ? this.state.assigned[assignment.id][slot] : 0;
    return (
      <DelegateSelect
        onChange={this._handleDelegateAssignment.bind(this, assignment.id, slot)}
        delegates={this.state.delegates}
        selectedDelegateId={selectedDelegateId}
      />
    );
  },

  _handleDelegateAssignment: function(assignmentId, slot, event) {
    var delegates = this.state.delegates;
    var assigned = this.state.assigned;
    var newDelegateId = event.target.value, oldDelegateId = 0;

    if (assignmentId in assigned) {
      oldDelegateId = assigned[assignmentId][slot];
      assigned[assignmentId][slot] = newDelegateId;
    } else {
      // This is the first time we're assigning a delegate to this assignment.
      var slots = new Array(2).fill(0);
      slots[slot] = newDelegateId;
      assigned[assignmentId] = slots;
    }

    for (var i = 0; i < delegates.length; i++) {
      if (delegates[i].id == newDelegateId) {
        // Assign the selected delegate
        delegates[i].assignment = assignmentId;
      } else if (delegates[i].id == oldDelegateId) {
        // Unassign the previous delegate from that assignment
        delegates[i].assignment = null;
      }
    }

    this.setState({
      delegates: delegates,
      assigned: assigned
    });
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

  _handleSave: function(event) {
    var school = CurrentUserStore.getCurrentUser().school;
    this.setState({loading: true});
    $.ajax ({
      type: 'PATCH',
      url: '/api/schools/' + school.id + '/delegates',
      data: JSON.stringify(this.state.delegates),
      success: this._handleSuccess,
      error: this._handleError,
    });
  },

  _handleFinalizedSuccess: function(data, status, jqXHR) {
    CurrentUserActions.updateSchool(jqXHR.responseJSON);
    this.setState({loading: false});
    this.history.pushState(null, '/advisor/assignments');
  },

  _handleAssignmentDeleteSuccess: function(data, status, jqXHR) {
    var assignments = this.state.assignments
    assignments = assignments.filter(function (assignment) {
      return assignment.id != jqXHR.responseJSON.id
    })
    this.setState({assignments: assignments})
    this.setState({loading: false});
    this.history.pushState(null, '/advisor/assignments');
  },

  _handleError: function(jqXHR, status, error) {
    window.alert("Something went wrong. Please try again.");
    this.setState({loading: false});
  },

   _handleSuccess: function(event) {
    this.setState({loading: false});
    this.history.pushState(null, '/advisor/assignments');
  }
});

module.exports = AdvisorAssignmentsView;
