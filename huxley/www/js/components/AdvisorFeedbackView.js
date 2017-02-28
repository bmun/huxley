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
    var assignments = AssignmentStore.getSchoolAssignments(schoolID).filter(assignment => !assignment.rejected);
    var feedback = this.prepareFeedback(delegates);
    return {
      feedback: feedback,
      assignments: assignments,
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

    this._assignmentsToken = AssignmentStore.addListener(() => {
      var schoolID = CurrentUserStore.getCurrentUser().school.id;
      this.setState({
        assignments: AssignmentStore.getSchoolAssignments(schoolID).filter(assignment => !assignment.rejected)
      });
    });

    this._delegatesToken = DelegateStore.addListener(() => {
      var schoolID = CurrentUserStore.getCurrentUser().school.id;
      var delegates = DelegateStore.getSchoolDelegates(schoolID);
      var feedback = this.prepareFeedback(delegates);
      this.setState({
        delegates: delegates,
        feedback: feedback
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
                  <th>Country</th>
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
    var assignments = this.state.assignments
    var committees = this.state.committees;
    var countries = this.state.countries;
    var feedback = this.state.feedback;
    return assignments.map(assignment => {
      var delegates = feedback[assignment.id];
      if (delegates == null) {
        return;
      }
      return (
        <tr>
          <td>{committees[assignment.committee].name}</td>
          <td>{countries[assignment.country].name}</td>
          <td>
            <input
              className="choice"
              type="checkbox"
              checked={delegates.session_one}
              disabled
            />
          </td>
          <td>
            <input
              className="choice"
              type="checkbox"
              checked={delegates.session_two}
              disabled
            />
          </td>
          <td>
            <input
              className="choice"
              type="checkbox"
              checked={delegates.session_three}
              disabled
            />
          </td>
          <td>
            <input
              className="choice"
              type="checkbox"
              checked={delegates.session_four}
              disabled
            />
          </td>
          <td>
            <textarea
              className="text-input"
              style={{"width": "95%"}}
              defaultValue={delegates.published_summary}
              disabled
            />
          </td>
        </tr>
      )
    });
  },


  /*
    To make it easier to assign and unassign delegates to assignments we maintain
    a state variable called "feedback". "feedback" is a dictionary whose key is
    an assignment id, and value is an array representing slots for two delegates
    to be feedback to it. This way we can easily manage the relationship from
    assignment to delegates via this object.
  */

  prepareFeedback: function(delegates) {
    var feedback = {};
      for (var delegate of delegates) {
        if (delegate.assignment) {
          if (!feedback[delegate.assignment]) {
            feedback[delegate.assignment] = delegate;
          }
        }
      }
      return feedback;
    },
});

module.exports = AdvisorFeedbackView;