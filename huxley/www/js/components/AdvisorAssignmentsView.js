/**
* Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var AssignmentActions = require('actions/AssignmentActions');
var AssignmentStore = require('stores/AssignmentStore');
var Button = require('components/Button');
var CommitteeStore = require('stores/CommitteeStore');
var ConferenceContext = require('components/ConferenceContext');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var CurrentUserActions = require('actions/CurrentUserActions');
var DelegateActions = require('actions/DelegateActions');
var DelegateSelect = require('components/DelegateSelect');
var DelegateStore = require('stores/DelegateStore');
var InnerView = require('components/InnerView');
var ServerAPI = require('lib/ServerAPI');

var AdvisorAssignmentsView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  getInitialState: function() {
    var schoolID = CurrentUserStore.getCurrentUser().school.id;
    var delegates = DelegateStore.getDelegates(schoolID);
    var assigned = this.prepareAssignedDelegates(delegates);
    return {
      assigned: assigned,
      assignments: AssignmentStore.getAssignments(schoolID).filter(assignment => !assignment.rejected),
      committees: CommitteeStore.getCommittees(),
      countries: CountryStore.getCountries(),
      delegates: delegates,
      loading: false
    };
  },

  componentDidMount: function() {
    this._committeesToken = CommitteeStore.addListener(() => {
      this.setState({committees: CommitteeStore.getCommittees()});
    });

    this._countriesToken = CountryStore.addListener(() => {
      this.setState({countries: CountryStore.getCountries()});
    });

    this._delegatesToken = DelegateStore.addListener(() => {
      var schoolID = CurrentUserStore.getCurrentUser().school.id;
      var delegates = DelegateStore.getDelegates(schoolID);
      var assigned = this.prepareAssignedDelegates(delegates);
      this.setState({
        delegates: delegates,
        assigned: assigned
      });
    });

    this._assignmentsToken = AssignmentStore.addListener(() => {
      var schoolID = CurrentUserStore.getCurrentUser().school.id;
      this.setState({
        assignments: AssignmentStore.getAssignments(schoolID).filter(assignment => !assignment.rejected)
      });
    });
  },

  componentWillUnmount: function() {
    this._committeesToken && this._committeesToken.remove();
    this._countriesToken && this._countriesToken.remove();
    this._delegatesToken && this._delegatesToken.remove();
    this._assignmentsToken && this._assignmentsToken.remove();
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
          info@bmun.org</a>. The assignment finalization deadline is January 23rd.
          After assignment finalization we will ask that you assign the
          delegates you have added in the delegates tab to the assignments
          given to you.
        </p>
        <form>
          <div className="table-container">
            <table>
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
          <Button
            color="green"
            onClick={finalized ? this._handleSave: this._handleFinalize}
            loading={this.state.loading}>
            {finalized? 'Save' : 'Finalize Assignments'}
          </Button>
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

  /*
    To make it easier to assign and unassign delegates to assignments we maintain
    a state variable called "assigned". "assigned" is a dictionary whose key is
    an assignment id, and value is an array representing slots for two delegates
    to be assigned to it. This way we can easily manage the relationship from
    assignment to delegates via this object.
  */
  prepareAssignedDelegates: function(delegates) {
    var assigned = {};
    for (var i = 0; i < delegates.length; i++) {
      if (delegates[i].assignment) {
        if (delegates[i].assignment in assigned) {
          assigned[delegates[i].assignment][1] = delegates[i].id;
        } else {
          var slots = [0, 0];
          slots[0] = delegates[i].id;
          assigned[delegates[i].assignment] = slots;
        }
      }
    }

    return assigned;
  },

  renderDelegateDropdown: function(assignment, slot) {
    var selectedDelegateID = assignment.id in this.state.assigned ? this.state.assigned[assignment.id][slot] : 0;
    return (
      <DelegateSelect
        onChange={this._handleDelegateAssignment.bind(this, assignment.id, slot)}
        delegates={this.state.delegates}
        selectedDelegateID={selectedDelegateID}
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
      var slots = [0, 0];
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
    var confirm = window.confirm("By pressing okay you are committing to the financial responsibility of each assignment. Are you sure you want to finalize assignments?");
    var school = CurrentUserStore.getCurrentUser().school;
    if (confirm) {
      CurrentUserActions.updateSchool(school.id, {
        assignments_finalized: true,
      }, this._handleError);
    }
  },

  _handleAssignmentDelete: function(assignment) {
    var confirm = window.confirm("Are you sure you want to delete this assignment?");
    if (confirm) {
      AssignmentActions.updateAssignment(assignment.id, {
        rejected: true,
      }, this._handleError);
    }
  },

  _handleSave: function(event) {
    var school = CurrentUserStore.getCurrentUser().school;
    DelegateActions.updateDelegates(school.id, this.state.delegates, this._handleError);
  },

  _handleError: function(response) {
    this.setState({loading: false});
    window.alert("Something went wrong. Please refresh your page and try again.");
  },
});

module.exports = AdvisorAssignmentsView;
