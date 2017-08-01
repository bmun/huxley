/**
* Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var Button = require('components/core/Button');
var AssignmentStore = require('stores/AssignmentStore');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateActions = require('actions/DelegateActions');
var DelegateStore = require('stores/DelegateStore');
var InnerView = require('components/InnerView');
var TextTemplate = require('components/core/TextTemplate');
var User = require('utils/User');

require('css/Table.less');
var ChairSummaryViewText = require('text/ChairSummaryViewText.md');

var ChairSummaryView = React.createClass({
  mixins: [ReactRouter.History],

  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
    var countries = CountryStore.getCountries();
    var delegates = DelegateStore.getCommitteeDelegates(user.committee);
    var summaries = {};
    for (var delegate of delegates) {
      summaries[delegate.assignment] = delegate.summary;
    }

    if (assignments.length && Object.keys(countries).length) {
      assignments.sort(
        (a1, a2) =>
          countries[a1.country].name < countries[a2.country].name ? -1 : 1,
      );
    }

    return {
      assignments: assignments,
      countries: countries,
      loadingSave: false,
      successSave: false,
      loadingPublish: false,
      successPublish: false,
      delegates: delegates,
      summaries: summaries,
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

    this._delegatesToken = DelegateStore.addListener(() => {
      var delegates = DelegateStore.getCommitteeDelegates(user.committee);
      var summaries = this.state.summaries;
      var update = {};
      for (var delegate of delegates) {
        update[delegate.assignment] = delegate.summary;
      }
      this.setState({
        delegates: delegates,
        summaries: {...summaries, ...update},
      });
    });

    this._assignmentsToken = AssignmentStore.addListener(() => {
      var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
      var countries = this.state.countries;
      if (Object.keys(countries).length) {
        assignments.sort(
          (a1, a2) =>
            countries[a1.country].name < countries[a2.country].name ? -1 : 1,
        );
      }
      this.setState({assignments: assignments});
    });

    this._countriesToken = CountryStore.addListener(() => {
      var assignments = this.state.assignments;
      var countries = CountryStore.getCountries();
      if (assignments.length) {
        assignments.sort(
          (a1, a2) =>
            countries[a1.country].name < countries[a2.country].name ? -1 : 1,
        );
      }
      this.setState({
        assignments: assignments,
        countries: countries,
      });
    });
  },

  componentWillUnmount() {
    this._successTimoutSave && clearTimeout(this._successTimeoutSave);
    this._successTimoutPublish && clearTimeout(this._successTimeoutPublish);
    this._countriesToken && this._countriesToken.remove();
    this._delegatesToken && this._delegatesToken.remove();
    this._assignmentsToken && this._assignmentsToken.remove();
    this._successTimeoutSave && clearTimeout(this._successTimeoutSave);
    this._successTimeoutPublish && clearTimeout(this._successTimeoutPublish);
  },

  render() {
    return (
      <InnerView>
        <TextTemplate>
          {ChairSummaryViewText}
        </TextTemplate>
        <form>
          <div className="table-container">
            <table style={{margin: '10px auto 0px auto'}}>
              <thead>
                <tr>
                  <th>Assignment</th>
                  <th style={{width: '65%'}}>Summary</th>
                </tr>
              </thead>
            </table>
            <div style={{overflowY: 'auto', maxHeight: '50vh'}}>
              <table
                className="table highlight-cells"
                style={{margin: '0px auto 20px auto'}}>
                <tbody>
                  {Object.keys(this.state.countries).length > 0
                    ? this.renderSummaryRows()
                    : <tr />}
                </tbody>
              </table>
            </div>
          </div>
          <Button
            color="green"
            onClick={this._handleSaveSummaries}
            loading={this.state.loadingSave}
            success={this.state.successSave}>
            Save
          </Button>
          <Button
            color="blue"
            onClick={this._handlePublishSummaries}
            loading={this.state.loadingPublish}
            success={this.state.successPublish}>
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
    assignments = assignments.filter(
      a => assignmentIDs.indexOf('' + a.id) > -1,
    );
    return assignments.map(assignment => {
      return (
        <tr key={assignment.id}>
          <td>
            {countries[assignment.country].name}
          </td>
          <td style={{width: '65%'}}>
            <textarea
              className="text-input"
              style={{width: '95%'}}
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
    var update = {};
    update[assignment.id] = newSummary;
    this.setState({summaries: {...summaries, ...update}});
  },

  _handleSaveSummaries(event) {
    this._successTimoutSave && clearTimeout(this._successTimeoutSave);
    this.setState({loadingSave: true});
    var committee = CurrentUserStore.getCurrentUser().committee;
    var delegates = this.state.delegates;
    var summaries = this.state.summaries;
    var toSave = [];
    for (var delegate of delegates) {
      var summary = summaries[delegate.assignment];
      if (delegate.summary != summary) {
        toSave.push({...delegate, summary});
      }
    }
    DelegateActions.updateCommitteeDelegates(
      committee,
      toSave,
      this._handleSuccessSave,
      this._handleErrorSave,
    );
    event.preventDefault();
  },

  _handlePublishSummaries(event) {
    var confirm = window.confirm(
      'By pressing ok, you are allowing advisors ' +
        'to read the summaries that you have written ' +
        'about their delegations. Please ensure ' +
        'there are no inappropriate comments or ' +
        'language in any of these summaries. If ' +
        'there is none and you are ready to publish ' +
        "your summaries to advisors, press 'ok' to " +
        'continue.',
    );
    if (confirm) {
      this._successTimoutPublish && clearTimeout(this._successTimeoutPublish);
      this.setState({loadingPublish: true});
      var committee = CurrentUserStore.getCurrentUser().committee;
      var delegates = this.state.delegates;
      var summaries = this.state.summaries;
      var toPublish = [];
      for (var delegate of delegates) {
        var summary = summaries[delegate.assignment];
        if (
          delegate.summary != summary ||
          delegate.published_summary != summary
        ) {
          toPublish.push({...delegate, summary, published_summary: summary});
        }
      }
      DelegateActions.updateCommitteeDelegates(
        committee,
        toPublish,
        this._handleSuccessPublish,
        this._handleErrorPublish,
      );
      event.preventDefault();
    }
  },

  _handleSuccessSave: function(response) {
    this.setState({
      loadingSave: false,
      successSave: true,
    });

    this._successTimeoutSave = setTimeout(
      () => this.setState({successSave: false}),
      2000,
    );
  },

  _handleErrorSave: function(response) {
    this.setState({loadingSave: false});
    window.alert(
      'Something went wrong. Please refresh your page and try again.',
    );
  },

  _handleSuccessPublish: function(response) {
    this.setState({
      loadingPublish: false,
      successPublish: true,
    });

    this._successTimeoutPublish = setTimeout(
      () => this.setState({successPublish: false}),
      2000,
    );
  },

  _handleErrorPublish: function(response) {
    this.setState({loadingPublish: false});
    window.alert(
      'Something went wrong. Please refresh your page and try again.',
    );
  },
});

module.exports = ChairSummaryView;
