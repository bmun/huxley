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
    return {
      assignments: AssignmentStore.getCommitteeAssignments(user.committee),
      countries: CountryStore.getCountries(),
      country_assignments: {},
      delegates: DelegateStore.getCommitteeDelegates(user.committee),
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
    this._mapAssignments();
    this._delegatesToken = DelegateStore.addListener(() => {
      this.setState({delegates: DelegateStore.getCommitteeDelegates(user.committee)});
      this._mapAssignments();
    });

    this._assignmentsToken = AssignmentStore.addListener(() => {
      this.setState({assignments: AssignmentStore.getCommitteeAssignments(user.committee)});
      this._mapAssignments();
    });

    this._countriesToken = CountryStore.addListener(() => {
      this.setState({countries: CountryStore.getCountries()});
    });
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
          <div className="table-container">
            <table className="table highlight-cells">
              <thead>
                <tr>
                  <th>Assignment</th>
                  <th>Summary</th>
                </tr>
              </thead>
              <tbody>
                {this.renderSummaryRows()}
              </tbody>
            </table>
          </div>
        </form>
        <div className="foot-bar" >
          <ul className="right">
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
          </ul>
        </div>
      </InnerView>
    );
  },

  renderSummaryRows() {
    var committeeCountries = Object.keys(this.state.country_assignments);
    var countries = this.state.countries;
    return committeeCountries.map(country => {
      var country_delegates = this.state.country_assignments[country];
      return (
        <tr key={country}>
          <td>
            {Object.keys(countries).length ? countries[country].name : country}
          </td>
          <td>
            <textarea
              className="text-input"
              style={{"width": "95%"}}
              rows="3"
              onChange={this._handleSummaryChange.bind(this, country)}
              defaultValue={country_delegates[0].summary}
            />
          </td>
        </tr>
      );
    });
  },

  _handleSummaryChange(country, event) {
    var newSummary = event.target.value;
    var country_assignments = this.state.country_assignments;
    var country_delegates = country_assignments[country];
    for (var delegate of country_delegates) {
      delegate.summary = newSummary;
    }
    this.setState({country_assignments: country_assignments});
  },

  _mapAssignments() {
    var user = CurrentUserStore.getCurrentUser();
    var country_assignments = {};
    var delegates = this.state.delegates;
    var assignments = this.state.assignments;
    for (var delegate of delegates) {
      var assignment = assignments.find(assignment => assignment.id == delegate.assignment);
      if (!assignment) continue;

      var countryID = assignment.country;
      if (countryID in country_assignments) {
        country_assignments[countryID].push(delegate);
        continue;
      }
      
      country_assignments[countryID] = [delegate];
    }

    this.setState({country_assignments: country_assignments});
  },

  _handleSaveSummaries(event) {
    var committee = CurrentUserStore.getCurrentUser().committee;
    var country_assignments = this.state.country_assignments;
    var delegates = [];
    for (var country in country_assignments) {
      delegates = delegates.concat(country_assignments[country]);
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
      var country_assignments = this.state.country_assignments;
      var delegates = [];
      for (var country in country_assignments) {
        delegates = delegates.concat(country_assignments[country]);
      }

      delegates.forEach(delegate => delegate.published_summary = delegate.summary);
      DelegateActions.updateCommitteeDelegates(committee, delegates);
    }
  },

});
    
module.exports = ChairSummaryView;
