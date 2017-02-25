/**
* Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var Button = require('components/Button');
var AssignmentStore = require('stores/AssignmentStore');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateActions = require('actions/DelegateActions');
var DelegateStore = require('stores/DelegateStore');
var InnerView = require('components/InnerView');
var User = require('utils/User');

var ChairSummaryView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
    var countries = CountryStore.getCountries();
    assignments.sort((a1, a2) => countries[a1.country].name < countries[a2.country].name ? -1 : 1);
    return {
      assignments: assignments,
      countries: countries,
      delegates: DelegateStore.getCommitteeDelegates(user.committee),
      summaries: {},
    };
  },

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isChair(user)) {
      this.history.pushState(null, '/');
    }
  },

  componentDidMount() {
    var user = CurrentUserStore.getCurrentUser();
    var delegates = this.state.delegates;
    var summaries = this.state.summaries;
    for (var delegate of delegates) {
      summaries[delegate.assignment] = delegate.summary;
    }

    this._delegatesToken = DelegateStore.addListener(() => {
      var delegates =  DelegateStore.getCommitteeDelegates(user.committee);
      for (var delegate of delegates) {
        summaries[delegate.assignment] = delegate.summary;
      }
      this.setState({
        delegates: delegates,
        summaries: summaries,
      });
    });

    this._assignmentsToken = AssignmentStore.addListener(() => {
      var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
      var countries = this.state.countries;
      if (Object.keys(countries).length > 0) {
        assignments.sort((a1, a2) => countries[a1.country].name < countries[a2.country].name ? -1 : 1);
      }
      this.setState({assignments: assignments});
    });

    this._countriesToken = CountryStore.addListener(() => {
      var assignments = this.state.assignments;
      var countries = CountryStore.getCountries;
      if (Object.keys(countries).length > 0) {
        assignments.sort((a1, a2) => countries[a1.country].name < countries[a2.country].name ? -1 : 1);
      }
      this.setState({
        assignments: assignments,
        countries: countries
      });
    });

    this.setState({summaries: summaries});
  },

  componentWillUnmount() {
    this._countriesToken && this._countriesToken.remove();
    this._delegatesToken && this._delegatesToken.remove();
    this._assignmentsToken && this._assignmentsToken.remove();
  },

  render() {
    return (
      <InnerView>
        <h2>Summaries</h2>
        <p>
          Here you can provide feedback for the delegates. You can save any 
          changes with the "Save" button and they will not become visible to 
          advisors until you next publish. Please note that clicking the 
          "Publish" button will allow advisors to read the summaries you have 
          written for their delegates. 
        </p>
        <p>
          <strong>
            Only one chair at a time should be logged in. Changes may be lost 
            otherwise.
          </strong>
        </p>
        <form>
          <div className="table-container"
            style={{'overflowY': 'auto', 'maxHeight': '50vh'}}>
            <table className="table highlight-cells">
              <thead>
                <tr>
                  <th>Assignment</th>
                  <th>Summary</th>
                </tr>
              </thead>
              <tbody>
                {
                  Object.keys(this.state.countries).length > 0 ?
                  this.renderSummaryRows() :
                  <tr></tr>
                }
              </tbody>
            </table>
          </div>
          <Button
            color="green"
            onClick={this._handleSaveSummaries}>
            Save
          </Button>
          <Button
            color="blue"
            onClick={this._handlePublishSummaries}>
            Publish
          </Button>
        </form>
      </InnerView>
    );
  },

  renderSummaryRows() {
    var assignments = this.state.assignments;
    var summaries = this.state.summaries;
    var assignmentIDs = Object.keys(summaries);
    var countries = this.state.countries;
    assignments = assignments.filter(a => assignmentIDs.indexOf(""+a.id) > -1);
    return assignments.map(assignment => {
      return (
        <tr key={assignment.id}>
          <td>
            {countries[assignment.country].name}
          </td>
          <td>
            <textarea
              className="text-input"
              style={{"width": "95%"}}
              rows="3"
              onChange={this._handleSummaryChange.bind(this, assignment)}
              defaultValue={summaries[assignment.id]}
            />
          </td>
        </tr>
      );
    });
  },

  _handleSummaryChange(assignment, event) {
    var newSummary = event.target.value;
    var summaries = this.state.summaries;
    summaries[assignment.id] = newSummary;
    this.setState({summaries: summaries});
  },

  _handleSaveSummaries(event) {
    var committee = CurrentUserStore.getCurrentUser().committee;
    var delegates = this.state.delegates;
    var summaries = this.state.summaries;
    for (var delegate of delegates) {
      delegate.summary = summaries[delegate.assignment];
    }
    DelegateActions.updateCommitteeDelegates(committee, delegates);
  },

  _handlePublishSummaries(event) {
    var confirm = window.confirm("By pressing ok, you are allowing advisors " +
                                 "to read the summaries that you have written " +
                                 "about their delegations. Please ensure " +
                                 "there are no inappropriate comments or " +
                                 "language in any of these summaries. If " +
                                 "there is none and you are ready to publish " +
                                 "your summaries to advisors, press 'ok' to " +
                                 "continue.");
    if (confirm) {
      var committee = CurrentUserStore.getCurrentUser().committee;
      var delegates = this.state.delegates;
      var summaries = this.state.summaries;
      for (var delegate of delegates) {
        delegate.summary = summaries[delegate.assignment];
      }
      delegates.forEach(delegate => delegate.published_summary = delegate.summary);
      DelegateActions.updateCommitteeDelegates(committee, delegates);
    }
  },

});
    
module.exports = ChairSummaryView;
