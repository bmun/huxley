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
              color="green"
              size="small"
              loading={this.state.loading}
              onClick={this._finalize}>
              Finalize Assignments
            </Button>
          </div>
        </form>
      </InnerView>
    );
  },

/*
  _finalize: function(e) {
    var elements = document.getElementsByName("test");
    var x = 0;
    for (var i=0; i<elements.length; i++) {
      if (elements[i].checked) {
        x = x + 1;
      }
    }
    window.alert(elements.length);
    window.alert(x);
  },
*/

  _finalize: function(e) {
    var committees = this.state.committees;
    var countries = this.state.countries;
    window.alert(committees.length);
    var elem = [];
    var x = 0;
    for (var i=0; i<10; i++) {
      for (var j=0; j<10; j++) {
        x = x + 1;
        var checkID = "test";
        var elem = document.getElementsByName(checkID);
        if (elem.length>0 && elem[0].checked) {
          x = x + 1;
        }
      }
    }
    window.alert(x);
  },

  renderAssignmentRows: function() {
    var committees = this.state.committees;
    var countries = this.state.countries;
    return this.state.assignments.map(function(assignment) {
      return (
        <tr>
          <td>{committees[assignment.committee].name}</td>
          <td>{countries[assignment.country].name}</td>
          <td>{committees[assignment.committee].delegation_size}</td>
          var checkID = committees[assignment.committee].name + countries[assignment.country].name
          <td><input name="test" type="checkbox"/></td>
        </tr>
      );
    });
  }
});

module.exports = AdvisorAssignmentsView;
