/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var Modal = require('react-modal');
var React = require('react');
var ReactRouter = require('react-router');

var _accessSafe = require('utils/_accessSafe');
var AssignmentStore = require('stores/AssignmentStore');
var Button = require('components/core/Button');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateActions = require('actions/DelegateActions');
var DelegateStore = require('stores/DelegateStore');
var ConferenceContext = require('components/ConferenceContext');
var CurrentUserActions = require('actions/CurrentUserActions');
var InnerView = require('components/InnerView');
var RegistrationStore = require('stores/RegistrationStore');
var ServerAPI = require('lib/ServerAPI');
var StatusLabel = require('components/core/StatusLabel');
var Table = require('components/core/Table');
var TextInput = require('components/core/TextInput');
var TextTemplate = require('components/core/TextTemplate');
var _checkDate = require('utils/_checkDate');
var _handleChange = require('utils/_handleChange');

require('css/Modal.less');
var AdvisorRosterViewText = require('text/AdvisorRosterViewText.md');
var AdvisorWaitlistText = require('text/AdvisorWaitlistText.md');

var AdvisorRosterView = React.createClass({
  mixins: [ReactRouter.History],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
  },

  getInitialState: function() {
    var schoolID = CurrentUserStore.getCurrentUser().school.id;
    var conferenceID = this.context.conference.session;
    return {
      delegates: DelegateStore.getSchoolDelegates(schoolID),
      registration: RegistrationStore.getRegistration(schoolID, conferenceID),
      assignments: AssignmentStore.getSchoolAssignments(schoolID).filter(
        assignment => !assignment.rejected,
      ),
      loading: false,
      modal_open: false,
      modal_name: '',
      modal_email: '',
      modal_onClick: null,
      errors: {},
    };
  },

  componentWillMount: function() {
    Modal.setAppElement('body');
  },

  componentDidMount: function() {
    var schoolID = CurrentUserStore.getCurrentUser().school.id;
    var conferenceID = this.context.conference.session;
    this._registrationToken = RegistrationStore.addListener(() => {
      this.setState({
        registration: RegistrationStore.getRegistration(schoolID, conferenceID),
      });
    });
    this._delegatesToken = DelegateStore.addListener(() => {
      this.setState({
        registration: RegistrationStore.getRegistration(schoolID, conferenceID),
        delegates: DelegateStore.getSchoolDelegates(schoolID),
        modal_open: false,
        loading: false,
      });
    });
  },

  componentWillUnmount: function() {
    this._registrationToken && this._registrationToken.remove();
    this._delegatesToken && this._delegatesToken.remove();
  },

  render: function() {
    var conference = this.context.conference;
    var registration = this.state.registration;
    var waitlisted =
      _accessSafe(registration, 'is_waitlisted') == null
        ? null
        : registration.is_waitlisted;
    var disableEdit = _checkDate();
    var addButton = disableEdit ? (
      <div />
    ) : (
      <Button
        color="green"
        onClick={this.openModal.bind(this, '', '', this._handleAddDelegate)}
        loading={this.state.loading}>
        Add Delegate
      </Button>
    );

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
          <TextTemplate>{AdvisorRosterViewText}</TextTemplate>
          <Table
            emptyMessage="You don't have any delegates in your roster."
            isEmpty={!this.state.delegates.length}>
            <thead>
              <tr>
                <th>Delegate</th>
                <th>Email</th>
                <th>Waiver</th>
                <th>Position Paper</th>
                <th>Edit</th>
                <th>Delete</th>
                <th>Reset Password</th>
              </tr>
            </thead>
            <tbody>{this.renderRosterRows()}</tbody>
          </Table>
          {addButton}
          <Modal
            isOpen={this.state.modal_open}
            className="content content-outer transparent ie-layout rounded"
            overlayClassName="modal-overlay">
            <form>
              <h3>Enter your delegate's information here</h3>
              <br />
              <TextInput
                placeholder="Name"
                onChange={_handleChange.bind(this, 'modal_name')}
                defaultValue={this.state.modal_name}
                value={this.state.modal_name}
              />
              {this.renderError('name')}
              <TextInput
                placeholder="Email"
                onChange={_handleChange.bind(this, 'modal_email')}
                defaultValue={this.state.modal_email}
                value={this.state.modal_email}
              />
              {this.renderError('email')}
              <hr />
              <div>
                <Button
                  onClick={this.state.modal_onClick}
                  color="green"
                  loading={this.state.loading}>
                  Save
                </Button>
                <Button onClick={this.closeModal} color="red">
                  Cancel
                </Button>
              </div>
            </form>
          </Modal>
        </InnerView>
      );
    }
  },

  renderRosterRows: function() {
    var committees = this.state.committees;
    var countries = this.state.countries;
    var assignments = this.state.assignments;
    var disableEdit = _checkDate();

    return this.state.delegates.map(
      function(delegate) {
        var editButton = disableEdit ? (
          <td />
        ) : (
          <td>
            <Button
              color="blue"
              size="small"
              onClick={this.openModal.bind(
                this,
                delegate.name,
                delegate.email,
                this._handleEditDelegate.bind(this, delegate),
              )}>
              Edit
            </Button>
          </td>
        );

        var deleteButton = disableEdit ? (
          <td />
        ) : (
          <td>
            <Button
              color="red"
              size="small"
              onClick={this._handleDeleteDelegate.bind(this, delegate)}>
              Delete
            </Button>
          </td>
        );


        const waiverCheck =
          delegate && delegate.waiver_submitted ? '\u2611' : '\u2610';

        const positionPaperCheck =
          delegate.assignment &&
          assignments[delegate.assignment - 1].paper &&
          assignments[delegate.assignment - 1].paper.file
            ? '\u2611'
            : '\u2610';




        return (
          <tr>
            <td>{delegate.name}</td>
            <td>{delegate.email}</td>
            <td>{waiverCheck}</td>
            <td>{positionPaperCheck}</td>
            {editButton}
            {deleteButton}
            <td>
              {delegate.assignment ? (
                <Button
                  color="yellow"
                  size="small"
                  onClick={this._handleDelegatePasswordChange.bind(
                    this,
                    delegate,
                  )}>
                  Reset Password
                </Button>
              ) : (
                <div />
              )}
            </td>
          </tr>
        );
      }.bind(this),
    );
  },

  openModal: function(name, email, fn, event) {
    this.setState({
      modal_open: true,
      modal_name: name,
      modal_email: email,
      modal_onClick: fn,
      errors: {},
    });
    event.preventDefault();
  },

  closeModal: function(event) {
    this.setState({modal_open: false});
    event.preventDefault();
  },

  renderError: function(field) {
    if (this.state.errors[field]) {
      return (
        <StatusLabel status="error">{this.state.errors[field]}</StatusLabel>
      );
    }

    return null;
  },

  _handleDeleteDelegate: function(delegate) {
    const confirmed = window.confirm(
      `Are you sure you want to delete this delegate (${delegate.name})?`,
    );
    if (confirmed) {
      DelegateActions.deleteDelegate(delegate.id, this._handleDeleteError);
    }
  },

  _handleAddDelegate: function(data) {
    this.setState({loading: true});
    var user = CurrentUserStore.getCurrentUser();
    ServerAPI.createDelegate(
      this.state.modal_name,
      this.state.modal_email,
      user.school.id,
    ).then(this._handleAddDelegateSuccess, this._handleError);
    event.preventDefault();
  },

  _handleEditDelegate: function(delegate) {
    var user = CurrentUserStore.getCurrentUser();
    this.setState({loading: true});
    var delta = {name: this.state.modal_name, email: this.state.modal_email};
    DelegateActions.updateDelegate(delegate.id, delta, this._handleError);
    event.preventDefault();
  },

  _handleDelegatePasswordChange: function(delegate) {
    ServerAPI.resetDelegatePassword(delegate.id).then(
      this._handlePasswordChangeSuccess,
      this._handlePasswordChangeError,
    );
  },

  _handleAddDelegateSuccess: function(response) {
    DelegateActions.addDelegate(response);
    this.setState({
      loading: false,
      modal_open: false,
    });
  },

  _handlePasswordChangeSuccess: function(response) {
    this.setState({
      loading: false,
      modal_open: false,
    });
    window.alert(`Password successfully reset.`);
  },

  _handlePasswordChangeError: function(response) {
    window.alert(`The passowrd could not be reset.`);
  },

  _handleDeleteError: function(response) {
    window.alert(
      `There was an issue processing your request. Please refresh you page and try again.`,
    );
  },

  _handleError: function(response) {
    this.setState({
      errors: response,
      loading: false,
      modal_open: true,
    });
  },
});

module.exports = AdvisorRosterView;