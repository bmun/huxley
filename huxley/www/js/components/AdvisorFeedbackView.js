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
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateStore = require('stores/DelegateStore');
var InnerView = require('components/InnerView');
var Table = require('components/Table');
var TextTemplate = require('components/TextTemplate');

var AdvisorFeedbackViewText = require('text/AdvisorFeedbackViewText.md');

var AdvisorFeedbackView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

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
        <TextTemplate>
          {AdvisorFeedbackViewText}
        </TextTemplate>
        <Table
          emptyMessage="You don't have any delegate feedback."
          isEmpty={!Object.keys(this.state.feedback).length}>
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
        </Table>
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

    The purpose of this is to allign the delegate objects with their respective
    assignment objects. We utilize an array called feedback, which has the delegate
    object situated at the assignment id's index of feedback. Originally, this was an
    array of dual arrays for dual delegations, but this has been deprecated since we use
    country name instead of delegate name.
  */

  prepareFeedback: function(delegates) {
    var feedback = {};
    for (var delegate of delegates) {
      if (delegate.assignment) {
          feedback[delegate.assignment] = delegate;
      }
    }
    return feedback;
  },
});

module.exports = AdvisorFeedbackView;
