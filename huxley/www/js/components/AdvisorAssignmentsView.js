/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var _accessSafe = require('utils/_accessSafe');
var AssignmentActions = require('actions/AssignmentActions');
var AssignmentStore = require('stores/AssignmentStore');
var Button = require('components/core/Button');
var _checkDate = require('utils/_checkDate');
var CommitteeStore = require('stores/CommitteeStore');
var ConferenceContext = require('components/ConferenceContext');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var CurrentUserActions = require('actions/CurrentUserActions');
var DelegateActions = require('actions/DelegateActions');
var DelegateSelect = require('components/DelegateSelect');
var DelegateStore = require('stores/DelegateStore');
var InnerView = require('components/InnerView');
var RegistrationActions = require('actions/RegistrationActions');
var RegistrationStore = require('stores/RegistrationStore');
var ServerAPI = require('lib/ServerAPI');
var Table = require('components/core/Table');
var TextTemplate = require('components/core/TextTemplate');

var AdvisorAssignmentsViewText = require('text/AdvisorAssignmentsViewText.md');
var AdvisorWaitlistText = require('text/AdvisorWaitlistText.md');

var AdvisorAssignmentsView = React.createClass({
  mixins: [ReactRouter.History],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
  },

  getInitialState: function() {
    var schoolID = CurrentUserStore.getCurrentUser().school.id;
    var delegates = DelegateStore.getSchoolDelegates(schoolID);
    var assigned = this.prepareAssignedDelegates(delegates);
    var conferenceID = this.context.conference.session;
    return {
      assigned: assigned,
      assignments: AssignmentStore.getSchoolAssignments(schoolID).filter(
        assignment => !assignment.rejected,
      ),
      committees: CommitteeStore.getCommittees(),
      countries: CountryStore.getCountries(),
      delegates: delegates,
      loading: false,
      success: false,
      registration: RegistrationStore.getRegistration(schoolID, conferenceID),
    };
  },

  componentDidMount: function() {
    var schoolID = CurrentUserStore.getCurrentUser().school.id;
    var conferenceID = this.context.conference.session;

    this._committeesToken = CommitteeStore.addListener(() => {
      this.setState({committees: CommitteeStore.getCommittees()});
    });

    this._countriesToken = CountryStore.addListener(() => {
      this.setState({countries: CountryStore.getCountries()});
    });

    this._delegatesToken = DelegateStore.addListener(() => {
      var schoolID = CurrentUserStore.getCurrentUser().school.id;
      var delegates = DelegateStore.getSchoolDelegates(schoolID);
      var assigned = this.prepareAssignedDelegates(delegates);
      this.setState({
        delegates: delegates,
        assigned: assigned,
      });
    });

    this._assignmentsToken = AssignmentStore.addListener(() => {
      this.setState({
        assignments: AssignmentStore.getSchoolAssignments(schoolID).filter(
          assignment => !assignment.rejected,
        ),
      });
    });

    this._registrationToken = RegistrationStore.addListener(() => {
      this.setState({
        registration: RegistrationStore.getRegistration(schoolID, conferenceID),
      });
    });
  },

  componentWillUnmount: function() {
    this._successTimout && clearTimeout(this._successTimeout);
    this._committeesToken && this._committeesToken.remove();
    this._countriesToken && this._countriesToken.remove();
    this._delegatesToken && this._delegatesToken.remove();
    this._assignmentsToken && this._assignmentsToken.remove();
    this._registrationToken && this._registrationToken.remove();
  },

  render: function() {
    var registration = this.state.registration;
    var waitlisted =
      _accessSafe(registration, 'is_waitlisted') == null
        ? null
        : registration.is_waitlisted;
    var finalized =
      _accessSafe(this.state.registration, 'assignments_finalized') == null
        ? false
        : this.state.registration.assignments_finalized;
    var committees = this.state.committees;
    var conference = this.context.conference;
    var countries = this.state.countries;
    var shouldRenderAssignments =
      Object.keys(committees).length > 0 &&
      Object.keys(countries).length > 0 &&
      this.state.assignments.length > 0 &&
      this.state.registration;

    if (waitlisted) {
      return (
        <InnerView>
          <TextTemplate
            conferenceSession={conference.session}
            conferenceExternal={conference.external}>
            {AdvisorWaitlistText}
          </TextTemplate>
        </InnerView>
      );
    } else {
      return (
        <InnerView>
          <TextTemplate conferenceSession={conference.session}>
            {AdvisorAssignmentsViewText}
          </TextTemplate>
          <Table
            emptyMessage="You don't have any assignments."
            isEmpty={!shouldRenderAssignments}>
            <thead>
              <tr>
                <th>Committee</th>
                <th>Country</th>
                <th>Delegation Size</th>
                <th>{finalized ? 'Delegate' : 'Delete Assignments'}</th>
                <th>{finalized ? 'Delegate' : ''}</th>
              </tr>
            </thead>
            <tbody>
              {shouldRenderAssignments ? this.renderAssignmentRows() : null}
            </tbody>
          </Table>
          <Button
            color="green"
            onClick={finalized ? this._handleSave : this._handleFinalize}
            loading={this.state.loading}
            success={this.state.success}>
            {finalized ? 'Save' : 'Finalize Assignments'}
          </Button>
        </InnerView>
      );
    }
  },

  renderAssignmentRows: function() {
    var committees = this.state.committees;
    var countries = this.state.countries;
    var finalized =
      _accessSafe(this.state.registration, 'assignments_finalized') == null
        ? false
        : this.state.registration.assignments_finalized;
    return this.state.assignments.map(
      function(assignment) {
        return (
          <tr>
            <td>{committees[assignment.committee].name}</td>
            <td>{countries[assignment.country].name}</td>
            <td>{committees[assignment.committee].delegation_size}</td>
            <td>
              {finalized ? (
                this.renderDelegateDropdown(assignment, 0)
              ) : (
                <Button
                  color="red"
                  size="small"
                  onClick={this._handleAssignmentDelete.bind(this, assignment)}>
                  Delete Assignment
                </Button>
              )}
            </td>
            <td>
              {finalized &&
              committees[assignment.committee].delegation_size == 2 ? (
                this.renderDelegateDropdown(assignment, 1)
              ) : (
                <div />
              )}
            </td>
          </tr>
        );
      }.bind(this),
    );
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
    var selectedDelegateID =
      assignment.id in this.state.assigned
        ? this.state.assigned[assignment.id][slot]
        : 0;
    var disableView = _checkDate();

    return (
      <DelegateSelect
        onChange={this._handleDelegateAssignment.bind(
          this,
          assignment.id,
          slot,
        )}
        delegates={this.state.delegates}
        selectedDelegateID={selectedDelegateID}
        disabled={disableView}
      />
    );
  },

  _handleDelegateAssignment: function(assignmentId, slot, event) {
    var delegates = this.state.delegates;
    var assigned = this.state.assigned;
    var newDelegateId = event.target.value,
      oldDelegateId = 0;

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
      assigned: assigned,
    });
  },

  _handleFinalize: function(event) {
    var confirm = window.confirm(
      'By pressing okay you are committing to the financial responsibility of each assignment. Are you sure you want to finalize assignments?',
    );
    if (confirm) {
      RegistrationActions.updateRegistration(
        this.state.registration.id,
        {
          assignments_finalized: true,
        },
        this._handleError,
      );
    }
  },

  _handleAssignmentDelete: function(assignment) {
    var confirm = window.confirm(
      'Are you sure you want to delete this assignment?',
    );
    if (confirm) {
      AssignmentActions.updateAssignment(
        assignment.id,
        {
          rejected: true,
        },
        this._handleError,
      );
    }
  },

  _handleSave: function(event) {
    this._successTimout && clearTimeout(this._successTimeout);
    this.setState({loading: true});
    var school = CurrentUserStore.getCurrentUser().school;
    DelegateActions.updateDelegates(
      school.id,
      this.state.delegates,
      this._handleSuccess,
      this._handleError,
    );
  },

  _handleSuccess: function(response) {
    this.setState({
      loading: false,
      success: true,
    });

    this._successTimeout = setTimeout(
      () => this.setState({success: false}),
      2000,
    );
  },

  _handleError: function(response) {
    this.setState({loading: false});
    window.alert(
      'Something went wrong. Please refresh your page and try again.',
    );
  },
});

module.exports = AdvisorAssignmentsView;
