/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Modal = require('react-modal');
var React = require('react');
var ReactRouter = require('react-router');

var AssignmentStore = require('../stores/AssignmentStore');
var Button = require('./Button');
var CommitteeStore = require('../stores/CommitteeStore');
var CountryStore = require('../stores/CountryStore');
var CurrentUserStore = require('../stores/CurrentUserStore');
var DelegateStore = require('../stores/DelegateStore');
var CurrentUserActions = require('../actions/CurrentUserActions');
var InnerView = require('./InnerView');
var TextInput = require('./TextInput');
var _handleChange = require('../utils/_handleChange');

const customStyles = {
  content : {
    top                   : '50%',
    left                  : '50%',
    right                 : 'auto',
    bottom                : 'auto',
    marginRight           : '-50%',
    transform             : 'translate(-50%, -50%)'
  }
};

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
          </div>
          <div className="tablemenu footer" />
          <Button
            color="green"
            onClick={this.openModal.bind(this, '', '', this._handleAddDelegate)}
            loading={this.state.loading}>
            Add Delegate
          </Button>
        </form>
        <Modal
          isOpen={this.state.modal_open}
          className="content content-outer transparent ie-layout rounded">
          <form>
            <h3>Enter your delegate's information here</h3>
            <br />
            <TextInput
              placeholder="Name"
              onChange={_handleChange.bind(this, 'modal_name')}
              value={this.state.modal_name}
            />
            {this.renderError("name")}
            <TextInput
              placeholder="Email (Optional)"
              onChange={_handleChange.bind(this, 'modal_email')}
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
    this.setState({loading: true});
    $.ajax ({
      type: 'DELETE',
      url: '/api/delegates/'+delegate.id,
      success: this._handleDelegateDeleteSuccess.bind(this, delegate.id),
      error: this._handleError,
    });
  },

  _handleAddDelegate: function(data) {
    this.setState({loading: true});
    var user = CurrentUserStore.getCurrentUser();
    $.ajax({
      type: 'POST',
      url: '/api/delegates/',
      data: JSON.stringify({
        name: this.state.modal_name,
        email: this.state.modal_email,
        school: user.school.id
      }),
      success: this._handleAddDelegateSuccess,
      error: this._handleError,
      dataType: 'json',
      contentType: 'application/json'
    });
    event.preventDefault();
  },

  _handleEditDelegate: function(delegate_id) {
    var user = CurrentUserStore.getCurrentUser();
    this.setState({loading: true});
    $.ajax ({
      type: 'PATCH',
      url: '/api/delegates/'+delegate_id,
      data: JSON.stringify({
        name: this.state.modal_name,
        email: this.state.modal_email,
        school: user.school.id
      }),
      success: this._handleEditDelegateSuccess,
      error: this._handleError,
      dataType: 'json',
      contentType: 'application/json'
    });
    event.preventDefault();
  },

  _handleDelegateDeleteSuccess: function(id, data, status, jqXHR) {
    var delegates = this.state.delegates;
    delegates = delegates.filter(function (delegate) {
        return delegate.id != id;
    });

    this.setState({
      delegates: delegates,
      loading: false
    });
  },

  _handleAddDelegateSuccess: function(data, status, jqXHR) {
    var delegates = this.state.delegates;
    delegates.push(data);

    this.setState({
      modal_open: false,
      loading: false
    });
  },

  _handleEditDelegateSuccess: function(data, status, jqXHR) {
    var delegates = this.state.delegates;
    for (var i = 0; i < delegates.length; i++) {
      if (delegates[i].id == data.id) {
        delegates[i] = data;
      }
    }

    this.setState({
      modal_open: false,
      delegates: delegates,
      loading: false
    });
  },

  _handleError: function(jqXHR, status, error) {
    var response = jqXHR.responseJSON;
    if (!response) {
      return;
    }

    this.setState({
      errors: response,
      loading: false
    });
  }

});

module.exports = AdvisorRosterView;
