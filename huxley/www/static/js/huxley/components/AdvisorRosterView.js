/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
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
      adding_delegate: false,
      editing_delegate: false,
      add_name: '',
      add_email: '',
      edit_name: '',
      edit_email: '',
      delegate_id: 0,
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
                  <th>Delete Delegate</th>
                </tr>
              </thead>
              <tbody>
                {this.renderRosterRows()}
              </tbody>
            </table>
          </div>
        </form>
        <Button
          color="green"
          onClick={this.openAddModal}
          loading={this.state.loading}>
          Add Delegate
        </Button>
        <Modal
          isOpen={this.state.adding_delegate}
          onAfterOpen={this.afterOpenModal}
          className="content content-outer transparent ie-layout rounded">
          <form>
            <h2>Add Delegate</h2>
            <br />
            <TextInput
              placeholder="Name"
              onChange={_handleChange.bind(this, 'add_name')}
              value={this.state.add_name}
            />
            <TextInput
              placeholder="Email (Optional)"
              onChange={_handleChange.bind(this, 'add_email')}
              value={this.state.add_email}
            />
            <hr />
            <div>
              <Button onClick={this._handleAddDelegate}
              color="green"
              loading={this.state.loading}>
              Save</Button>
              <Button
                onClick={this.closeModal.bind(this, 'add')}
                color="red">
                Cancel
              </Button>
            </div>
          </form>
        </Modal>
        <Modal
          isOpen={this.state.editing_delegate}
          onAfterOpen={this.afterOpenModal}
          className="content content-outer transparent ie-layout rounded">
          <form>
            <h2>Edit Delegate</h2>
            <br />
            <TextInput
              placeholder="Name"
              onChange={_handleChange.bind(this, 'edit_name')}
              value={this.state.edit_name}
            />
            <TextInput
               placeholder="Email (Optional)"
               onChange={_handleChange.bind(this, 'edit_email')}
               value={this.state.edit_email}
            />
            <hr />
            <div>
              <Button onClick={this._handleEditDelegate}
              color="green"
              loading={this.state.loading}>
              Save</Button>
              <Button
                onClick={this.closeModal.bind(this, 'edit')}
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
    console.dir(this.state.delegates[0])
    return this.state.delegates.map(function(delegate) {
      return (
        <tr>
          <td>{delegate.name}</td>
          <td>{delegate.email}</td>
          <td>{delegate.summary}</td>
          <td>
            <Button color="blue"
                    size="small"
                    onClick={this.openEditModal.bind(this, delegate)}>
              Edit
            </Button>
            <Button color="red"
                    size="small"
                    onClick={this._handleDeleteDelegate.bind(this, delegate)}>
              Delete
            </Button>
          </td>
        </tr>
      )
    }.bind(this));
  },
 
  openAddModal: function() {
    this.setState({adding_delegate: true});
  },

  openEditModal: function(delegate) {
    this.setState({editing_delegate: true});
    this.setState({delegate_id: delegate.id});
    this.setState({edit_name: delegate.name});
    this.setState({edit_email: delegate.email});
  },
 
  afterOpenModal: function() {
    // references are now sync'd and can be accessed.
    this.refs.subtitle.style.color = '#f00';
  },
 
  closeModal: function(modal) {
    if (modal === "add") {
      this.setState({adding_delegate: false});
    } else if (modal === "edit") {
      this.setState({editing_delegate: false});
    }
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
        name: this.state.add_name,
        email: this.state.add_email,
        school: user.school.id
      }),
      success: this._handleAddDelegateSuccess,
      error: this._handleError,
      dataType: 'json',
      contentType: 'application/json'
    });
    event.preventDefault();
  },

  _handleEditDelegate: function(delegate) {
    var user = CurrentUserStore.getCurrentUser();
    this.setState({loading: true});
    $.ajax ({
      type: 'PATCH',
      url: '/api/delegates/'+this.state.delegate_id,
      data: JSON.stringify({
        name: this.state.edit_name,
        email: this.state.edit_email,
        school: user.school.id
      }),
      success: this._handleEditDelegateSuccess.bind(this, delegate.id),
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
    this.setState({delegates: delegates});
    this.setState({loading: false});
    this.history.pushState(null, '/advisor/roster');
  },
 
  _handleAddDelegateSuccess: function(data, status, jqXHR) {
    var delegates = this.state.delegates;
    delegates.push(data);
    this.setState({adding_delegate: false});
    this.setState({loading: false});
    this.history.pushState(null, '/advisor/roster');
  },

  _handleEditDelegateSuccess: function(id, data, status, jqXHR) {
    var delegates = this.state.delegates;
    delegates = delegates.filter(function (delegate) {
        return delegate.id != id;
    });
    this.setState({editing_delegate: false});
    this.setState({delegates: delegates});
    this.setState({loading: false});
    this.history.pushState(null, '/advisor/roster');
  },
 
  _handleError: function(jqXHR, status, error) {
    console.log("error");
    console.log(error);
    var response = jqXHR.responseJSON;
    if (!response) {
      return;
    }
 
    this.setState({
      loading: false
    }.bind(this));
  }
 
});
 
module.exports = AdvisorRosterView;
