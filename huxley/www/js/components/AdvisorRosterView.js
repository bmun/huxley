/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var Modal = require('react-modal');
var React = require('react');
var ReactRouter = require('react-router');

var AssignmentStore = require('stores/AssignmentStore');
var Button = require('components/Button');
var CommitteeStore = require('stores/CommitteeStore');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateActions = require('actions/DelegateActions');
var DelegateStore = require('stores/DelegateStore');
var CurrentUserActions = require('actions/CurrentUserActions');
var InnerView = require('components/InnerView');
var ServerAPI = require('lib/ServerAPI');
var TextInput = require('components/TextInput');
var _handleChange = require('utils/_handleChange');

var AdvisorRosterView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

  getInitialState: function() {
    return {
      assignments: [],
      delegates: [],
      loading: false,
      modal_open: false,
      modal_name: '',
      modal_email: '',
      modal_onClick: null,
      errors: {}
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

    Modal.setAppElement('body')
  },

  componentDidMount: function() {
    DelegateStore.addListener(function() {
      var schoolID =  CurrentUserStore.getCurrentUser().school.id;
      var delegates = DelegateStore.getDelegates(schoolID);
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
          <div className="table-container">
            <table className="table highlight-cells">
              <thead>
                <tr>
                  <th>Delegate</th>
                  <th>Email</th>
                  <th>Summary</th>
                  <th>Edit</th>
                  <th>Delete</th>
                </tr>
              </thead>
              <tbody>
                {this.renderRosterRows()}
              </tbody>
            </table>
            {this.renderEmptyMessage()}
          </div>
          <Button
            color="green"
            onClick={this.openModal.bind(this, '', '', this._handleAddDelegate)}
            loading={this.state.loading}>
            Add Delegate
          </Button>
        </form>
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
            {this.renderError("name")}
            <TextInput
              placeholder="Email (Optional)"
              onChange={_handleChange.bind(this, 'modal_email')}
              defaultValue={this.state.modal_email}
              value={this.state.modal_email}
            />
            {this.renderError("email")}
            <hr />
            <div>
              <Button
                onClick={this.state.modal_onClick}
                color="green"
                loading={this.state.loading}>
                Save
              </Button>
              <Button
                onClick={this.closeModal}
                color="red">
                Cancel
              </Button>
            </div>
          </form>
        </Modal>
      </InnerView>
    );
  },

  renderRosterRows: function() {
    var committees = this.state.committees;
    var countries = this.state.countries;
    return this.state.delegates.map(function(delegate) {
      return (
        <tr>
          <td>{delegate.name}</td>
          <td>{delegate.email}</td>
          <td>{delegate.summary}</td>
          <td>
            <Button
              color="blue"
              size="small"
              onClick={this.openModal.bind(
                this,
                delegate.name,
                delegate.email,
                this._handleEditDelegate.bind(this, delegate.id))}>
              Edit
            </Button>
          </td>
          <td>
            <Button
              color="red"
              size="small"
              onClick={this._handleDeleteDelegate.bind(this, delegate)}>
              Delete
            </Button>
          </td>
        </tr>
      )
    }.bind(this));
  },

  renderEmptyMessage: function() {
    if (this.state.delegates.length) {
      return null;
    }
    return (
      <div className="empty">
        {"You don't have any delegates in your roster."}
      </div>
    );
  },

  openModal: function(name, email, fn) {
    this.setState({
      modal_open: true,
      modal_name: name,
      modal_email: email,
      modal_onClick: fn,
      errors: {}
    });
  },

  closeModal: function() {
    this.setState({modal_open: false});
  },

  renderError: function(field) {
    if (this.state.errors[field]) {
      return (
        <label className="hint error">
          {this.state.errors[field]}
        </label>
      );
    }

    return null;
  },

  _handleDeleteDelegate: function(delegate) {
    const confirmed = window.confirm(
      `Are you sure you want to delete this delegate (${delegate.name})?`
    );
    if (confirmed) {
      DelegateActions.deleteDelegate(delegate);
    }
  },

  _handleAddDelegate: function(data) {
    this.setState({loading: true});
    var user = CurrentUserStore.getCurrentUser();
    ServerAPI.createDelegate(
      this.state.modal_name,
      this.state.modal_email,
      user.school.id
    ).then(this._handleAddDelegateSuccess, this._handleError);
    event.preventDefault();
  },

  _handleEditDelegate: function(delegateID) {
    var user = CurrentUserStore.getCurrentUser();
    this.setState({loading: true});
    ServerAPI.updateDelegate(delegateID, {
      name: this.state.modal_name,
      email: this.state.modal_email,
      school: user.school.id,
    }).then(this._handleEditDelegateSuccess, this._handleError);
    event.preventDefault();
  },

  _handleDelegateDeleteSuccess: function(id, response) {
    this.setState({
      delegates: this.state.delegates.filter((delegate) => delegate.id != id),
      loading: false,
    });
  },

  _handleAddDelegateSuccess: function(response) {
    this.setState({
      delegates: this.state.delegates.concat(response),
      loading: false,
      modal_open: false,
    });
  },

  _handleEditDelegateSuccess: function(response) {
    var delegates = this.state.delegates;
    for (var i = 0; i < delegates.length; i++) {
      if (delegates[i].id == response.id) {
        delegates[i] = response;
      }
    }

    this.setState({
      modal_open: false,
      delegates: delegates,
      loading: false
    });
  },

  _handleError: function(response) {
    this.setState({
      errors: response,
      loading: false
    });
  }

});

module.exports = AdvisorRosterView;
