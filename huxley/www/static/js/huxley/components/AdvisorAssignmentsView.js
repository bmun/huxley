/**
* Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
*
* @jsx React.DOM
+*/

'use strict';

var $ = require('jquery');
var React = require('react');

var AssignmentStore = require('../stores/AssignmentStore');
var Button = require('./Button');
var CommitteeStore = require('../stores/CommitteeStore');
var CountryStore = require('../stores/CountryStore');
var InnerView = require('./InnerView');

var AdvisorAssignmentsView = React.createClass({
  getInitialState: function() {
    return {
      assignments: [],
      committees: {},
      countries: {}
    };
  },

  componentWillMount: function() {
    var user = this.props.user.getData();
    AssignmentStore.getAssignments(user.school.id, function(assignments) {
      this.setState({assignments: assignments});
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
    var school = this.props.user.getSchool();
    if (school.assignments_finalized) {
      return (
        <InnerView>
          <h2>Roster</h2>
          <p>
            Your assignments have been finalized! If you
            would like to request more slots, please email <a href="mailto:info@bmun.org">
            info@bmun.org</a>.
          </p>
          <form>
            <div className="tablemenu header" />
            <div className="table-container">
              <table className="table highlight-cells">
                <tr>
                  <th>Committee</th>
                  <th>Country</th>
                  <th>Delegation Size</th>
                </tr>
                {this.renderAssignmentRows()}
              </table>
            </div>
            <div className="tablemenu footer">
            </div>
          </form>
        </InnerView>
      );
    } else {
      return (
        <InnerView>
          <h2>Roster</h2>
          <p>
            Here you can view your tentative assignments for BMUN 63. If you
            would like to request more slots, please email <a href="mailto:info@bmun.org">
            info@bmun.org</a>. In the coming months
            we will ask that you finalize your assignment roster and input your
            delegates' names.
          </p>
          <form>
            <div className="tablemenu header" />
            <div className="table-container">
              <table className="table highlight-cells">
                <tr>
                  <th>Committee</th>
                  <th>Country</th>
                  <th>Delegation Size</th>
                </tr>
                {this.renderAssignmentRows()}
              </table>
            </div>
            <div className="tablemenu footer">
              <Button
                id="finalize"
                color="green"
                size="small"
                loading={this.state.loading}
                onClick={this._handleClick}>
                Finalize Assignments
              </Button>
            </div>
          </form>
        </InnerView>
      );
    }
  },

  _handleClick: function(event) {
    this.setState({loading: true});
    var user = this.props.user.getData();
    var school = this.props.user.getSchool();
    var elements = document.getElementsByTagName("input");
    var assignList = [];
    for (var i=0; i<elements.length; i++) {
      if (elements[i].getAttribute("type") == 'checkbox') {
        if (!elements[i].checked) {
          assignList.push(elements[i].getAttribute("name"));
        }
      }
    }
    $.ajax({
      type: 'POST',
      url: '/api/schools/' + school.id + '/finalize/',
      data: JSON.stringify(assignList, null, 2),
      success: this._handleSuccess,
      error: this._handleError,
      dataType: 'text'
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    this.setState({loading: false});
    location.reload();
  },

  _handleError: function(jqXHR, status, error) {
    window.alert("Something went wrong. Please try again.");
    this.setState({loading: false});
  },

  renderAssignmentRows: function() {
    var committees = this.state.committees;
    var countries = this.state.countries;
    var school = this.props.user.getSchool();
    if (school.assignments_finalized) {
      return this.state.assignments.map(function(assignment) {
        return (
          <tr>
            <td>{committees[assignment.committee].name}</td>
            <td>{countries[assignment.country].name}</td>
            <td>{committees[assignment.committee].delegation_size}</td>
          </tr>
        );
      });
    } else {
      return this.state.assignments.map(function(assignment) {
        return (
          <tr>
            <td>{committees[assignment.committee].name}</td>
            <td>{countries[assignment.country].name}</td>
            <td>{committees[assignment.committee].delegation_size}</td>
            <td><input name={assignment.id} type="checkbox"/></td>
          </tr>
        );
      });
    }
  }
});

module.exports = AdvisorAssignmentsView;
