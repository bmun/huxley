/**
* Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
*
* @jsx React.DOM
+*/

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
          onClick={this.openModal}
          loading={this.state.loading}>
          Add Delegate
        </Button>
        <Modal
          isOpen={this.state.adding_delegate}
          onAfterOpen={this.afterOpenModal}
          onRequestClose={this.closeModal}
          style={customStyles} >
          <h2 ref="subtitle">Hello</h2>
          <button onClick={this.closeModal}>close</button>
          <div>I am a modal</div>
          <form>
            <input />
            <button>tab navigation</button>
            <button>stays</button>
            <button>inside</button>
            <button>the modal</button>
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

  _handleAddDelegate: function() {
    this.setState({adding_delegate: true});
    return (
      <Modal
        isOpen={this.state.adding_delegate}
        closeTimeoutMS={5}>
        <h1>Modal Content</h1>
        <p>Etc.</p>
      </Modal>
    );
  },

  openModal: function() {
    this.setState({adding_delegate: true});
  },

  afterOpenModal: function() {
    // references are now sync'd and can be accessed.
    this.refs.subtitle.style.color = '#f00';
  },

  closeModal: function() {
    this.setState({adding_delegate: false});
  },

  _handleDeleteDelegate: function(delegate) {
    this.setState({loading: true});
    $.ajax ({
      type: 'DELETE',
      url: '/api/delegates/'+delegate.id,
      success: this._handleDelegateDeleteSuccess,
      error: this._handleError,
    });
  },

  _handleDelegateDeleteSuccess: function(data, status, jqXHR) {
    var delegates = this.state.delegates
    delegates = delegates.filter(function (delegate) {
      return delegate.id != jqXHR.responseJSON.delegate.id
    });
    this.setState({delegates: delegates})
    this.setState({loading: false});
    this.history.pushState(null, '/advisor/roster');
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
