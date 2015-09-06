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
      countries: {},
      finalizing: false
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
                <th>{school.assignments_finalized ? "finalized" : "Relinquish Assignment"}</th>
              </tr>
              {this.renderAssignmentRows()}
            </table>
          </div>
          <div className="tablemenu footer" />
        </form>
        {school.assignments_finalized ? <div> </div>: <div className="center"><Button color="green" size="large"> Finalize Assignments </Button></div>}
      </InnerView>
    );
  },

  renderAssignmentRows: function() {
    var school = this.props.user.getSchool();
    var committees = this.state.committees;
    var countries = this.state.countries;
    return this.state.assignments.map(function(assignment) {
      return (
        <tr>
          <td>{committees[assignment.committee].name}</td>
          <td>{countries[assignment.country].name}</td>
          <td>{committees[assignment.committee].delegation_size}</td>
          <td>{school.assignments_finalized ?
            <input className="text" type="text" placeholder="Assigned Delegate"/> :
            <Button color="red" size="small"> Relinquish </Button>}
          </td>
        </tr>
      );
    });
  },
});

module.exports = AdvisorAssignmentsView;
