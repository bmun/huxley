/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var Modal = require('react-modal');
var React = require('react');
var ReactRouter = require('react-router');

var Button = require('components/Button');
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
    var schoolID = CurrentUserStore.getCurrentUser().school.id;
    return {
      delegates: DelegateStore.getSchoolDelegates(schoolID),
      loading: false,
      modal_open: false,
      modal_name: '',
      modal_email: '',
      modal_onClick: null,
      errors: {}
    };
  },

  componentWillMount: function() {
    Modal.setAppElement('body')
  },

  componentDidMount: function() {
    this._delegatesToken = DelegateStore.addListener(() => {
      var schoolID = CurrentUserStore.getCurrentUser().school.id;
      this.setState({
        delegates: DelegateStore.getSchoolDelegates(schoolID),
        modal_open: false,
        loading: false
      });
    });
  },

  componentWillUnmount: function() {
    this._delegatesToken && this._delegatesToken.remove();
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
          <td>
            <Button
              color="blue"
              size="small"
              onClick={this.openModal.bind(
                this,
                delegate.name,
                delegate.email,
                this._handleEditDelegate.bind(this, delegate))}>
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
      DelegateActions.deleteDelegate(delegate.id, this._handleDeleteError);
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

  _handleEditDelegate: function(delegate) {
    var user = CurrentUserStore.getCurrentUser();
    this.setState({loading: true});
    var delta = {name: this.state.modal_name, email: this.state.modal_email};
    DelegateActions.updateDelegate(delegate.id, delta, this._handleError);
    event.preventDefault();
  },

  _handleAddDelegateSuccess: function(response) {
    DelegateActions.addDelegate(response);
    this.setState({
      loading: false,
      modal_open: false,
    });
  },

  _handleDeleteError: function(response) {
    window.alert(
      `There was an issue processing your request. Please refresh you page and try again.`
    );
  },

  _handleError: function(response) {
    this.setState({
      errors: response,
      loading: false,
      modal_open: true
    });
  }

});

module.exports = AdvisorRosterView;
