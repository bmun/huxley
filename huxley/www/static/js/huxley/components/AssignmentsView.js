/**
* Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
*
* @jsx React.DOM
+*/

'use strict';

var console = require('console');
var $ = require('jquery');

var React = require('react');
var AdvisorView = require('./AdvisorView');
var AssignmentStore = require('../stores/AssignmentStore');
var CommitteeStore = require('../stores/CommitteeStore');
var CountryStore = require('../stores/CountryStore');

var AssignmentsView = React.createClass({
  getInitialState: function() {
    return {
      assignments: [],
      committees: [],
      countries: []
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

  render: function(){
    return(
      <AdvisorView user={this.props.user}>
        <form id="welcomepage">
          <div className="tablemenu header">
          </div>
          <div id="welcomeinfocontainer" className="table-container">
            <table id="welcomeinfo" className="table highlight-cells">
              <tr>
                <th>Committee</th>
                <th>Country</th>
                <th>Delegation Size</th>
              </tr>
              {this.generateAssignmentRows()}
            </table>
          </div>
          <div className="tablemenu footer">
          </div>
        </form>
      </AdvisorView>
    );
  },

  generateAssignmentRows: function() {
    var rows = [];
    for (var i = 0; i < this.state.assignments.length; i++) {
      rows.push(<tr>
        <td>{this.state.committees[this.state.assignments[i].committee].name}</td>
        <td>{this.state.countries[this.state.assignments[i].country].name}</td>
        <td>{this.state.committees[this.state.assignments[i].committee].delegation_size}</td>
      </tr>);
    }
    return rows;
  }
});

module.exports = AssignmentsView;
