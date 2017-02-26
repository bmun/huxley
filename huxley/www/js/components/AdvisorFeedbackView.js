/**
* Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var AssignmentActions = require('actions/AssignmentActions');
var AssignmentStore = require('stores/AssignmentStore');
var Button = require('components/Button');
var CommitteeStore = require('stores/CommitteeStore');
var ConferenceContext = require('components/ConferenceContext');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateStore = require('stores/DelegateStore');
var InnerView = require('components/InnerView');
var ServerAPI = require('lib/ServerAPI');

var AdvisorFeedbackView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  getInitialState: function() {
    var schoolID = CurrentUserStore.getCurrentUser().school.id;
    var delegates = DelegateStore.getSchoolDelegates(schoolID);
    var assigned = this.prepareAssignedDelegates(delegates);
    return {
      assigned: assigned,
      assignments: AssignmentStore.getSchoolAssignments(schoolID).filter(assignment => !assignment.rejected),
      committees: CommitteeStore.getCommittees(),
      countries: CountryStore.getCountries(),
      delegates: delegates,
      loading: false
    };
  },

  componentDidMount: function() {
    this._committeesToken = CommitteeStore.addListener(() => {
      this.setState({committees: CommitteeStore.getCommittees()});
    });

    this._countriesToken = CountryStore.addListener(() => {
      this.setState({countries: CountryStore.getCountries()});
    });

    this._delegatesToken = DelegateStore.addListener(() => {
      var schoolID = CurrentUserStore.getCurrentUser().school.id;
      var delegates = DelegateStore.getSchoolDelegates(schoolID);
      var assigned = this.prepareAssignedDelegates(delegates);
      this.setState({
        delegates: delegates,
        assigned: assigned
      });
    });

    this._assignmentsToken = AssignmentStore.addListener(() => {
      var schoolID = CurrentUserStore.getCurrentUser().school.id;
      this.setState({
        assignments: AssignmentStore.getSchoolAssignments(schoolID).filter(assignment => !assignment.rejected)
      });
    });
  },

  componentWillUnmount: function() {
    this._committeesToken && this._committeesToken.remove();
    this._countriesToken && this._countriesToken.remove();
    this._delegatesToken && this._delegatesToken.remove();
    this._assignmentsToken && this._assignmentsToken.remove();
  },

  render: function() {
    return (
      <InnerView>
        <h2>Feedback</h2>
        <p>
          Here you can view chairs feedback on your delegates, as well as their attendance.
        </p>
          <div className="table-container">
            <table className="table highlight-cells">
              <thead>
                <tr>
                  <th>Committee</th>
                  <th>Delegates</th>
                  <th>1</th>
                  <th>2</th>
                  <th>3</th>
                  <th>4</th>
                  <th>Summary</th>
                </tr>
              </thead>
              <tbody>
                {this.renderAssignmentRows()}
              </tbody>
            </table>
          </div>
      </InnerView>
    );
  },

  renderAssignmentRows: function() {
    var committees = this.state.committees;
    var countries = this.state.countries;
    var assigned = this.state.assigned;
    return this.state.assignments.map(function(assignment) {
      var delegates = assigned[assignment.id];
      if (delegates == null) {
        return;
      }
      return (
        <tr>
          <td>{committees[assignment.committee].name}</td>
          <td>{delegates[1] == 0 ?
            delegates[0].name :
            delegates[0].name + ', ' + delegates[1].name
          }</td>
          <td>
            <input
              className="choice"
              type="checkbox"
              checked={delegates[0].session_one}
              disabled
            />
          </td>
          <td>
            <input
              className="choice"
              type="checkbox"
              checked={delegates[0].session_two}
              disabled
            />
          </td>
          <td>
            <input
              className="choice"
              type="checkbox"
              checked={delegates[0].session_three}
              disabled
            />
          </td>
          <td>
            <input
              className="choice"
              type="checkbox"
              checked={delegates[0].session_four}
              disabled
            />
          </td>
          <textarea
              className="text-input"
              style={{"width": "95%"}}
              defaultValue={delegates[0].published_summary}
              disabled
            />
        </tr>
      )
    }.bind(this));
  },


  /*
    To make it easier to assign and unassign delegates to assignments we maintain
    a state variable called "assigned". "assigned" is a dictionary whose key is
    an assignment id, and value is an array representing slots for two delegates
    to be assigned to it. This way we can easily manage the relationship from
    assignment to delegates via this object.
  */

  prepareAssignedDelegates: function(delegates) {
    var assigned = {};
    for (var i = 0; i < delegates.length; i++) {
      if (delegates[i].assignment) {
        if (assigned[delegates[i].assignment]) {
          assigned[delegates[i].assignment][1] = delegates[i]; 
        } else {
          var slots = [0, 0, 0];
          slots[0] = delegates[i];
          slots[2] = delegates[i].assignment;
          assigned[delegates[i].assignment] = slots;
        }
      }
    }

    return assigned;
  },
});

module.exports = AdvisorFeedbackView;