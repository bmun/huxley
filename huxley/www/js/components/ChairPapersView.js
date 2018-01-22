/**
* Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var Button = require('components/core/Button');
var AssignmentStore = require('stores/AssignmentStore');
var CommitteeStore = require('stores/CommitteeStore');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateActions = require('actions/DelegateActions');
var DelegationAttendanceRow = require('components/DelegationAttendanceRow');
var DelegateStore = require('stores/DelegateStore');
var InnerView = require('components/InnerView');
var PaperAssignmentList = require('components/PaperAssignmentList');
var PaperGradeTable = require('components/PaperGradeTable');
var PositionPaperActions = require('actions/PositionPaperActions');
var PositionPaperStore = require('stores/PositionPaperStore');
var TextTemplate = require('components/core/TextTemplate');
var User = require('utils/User');

var ServerAPI = require('lib/ServerAPI');

require('css/Table.less');
var ChairAttendanceViewText = require('text/ChairAttendanceViewText.md');

var ChairPapersView = React.createClass({
  mixins: [ReactRouter.History],

  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
    var countries = CountryStore.getCountries();
    var committees = CommitteeStore.getCommittees();
    var papers = {};
    var files = {};
    if (assignments.length) {
      PositionPaperStore.getPositionPaperFile(assignments[0].paper.id, assignments[0].paper.file);
    }

    if (assignments.length && Object.keys(countries).length) {
      assignments.sort(
        (a1, a2) =>
          countries[a1.country].name < countries[a2.country].name ? -1 : 1,
      );
      for (var a of assignments) {
        papers[a.paper.id] = a.paper;
      }
    }

    return {
      loading: false,
      success: false,
      assignments: assignments,
      committees: committees,
      countries: countries,
      papers: papers,
      current_assignment: null,
      files: files,
      errors: {},
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

    this._assignmentsToken = AssignmentStore.addListener(() => {
      var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
      var countries = this.state.countries;
      var papers = {};
      PositionPaperStore.getPositionPaperFile(assignments[0].paper.id, assignments[0].paper.file);
      if (Object.keys(countries).length) {
        assignments.sort(
          (a1, a2) =>
            countries[a1.country].name < countries[a2.country].name ? -1 : 1,
        );
        for (var a of assignments) {
          papers[a.paper.id] = a.paper;
        }
      }
      this.setState({
        assignments: assignments,
        papers: papers
      });
    });

    this._countriesToken = CountryStore.addListener(() => {
      var assignments = this.state.assignments;
      var countries = CountryStore.getCountries();
      var papers = {};
      if (assignments.length) {
        assignments.sort(
          (a1, a2) =>
            countries[a1.country].name < countries[a2.country].name ? -1 : 1,
        );
        for (var a of assignments) {
          papers[a.paper.id] = a.paper;
        }
      }
      this.setState({
        assignments: assignments,
        countries: countries,
        papers: papers
      });
    });

    this._committeesToken = CommitteeStore.addListener(() => {
      this.setState({committees: CommitteeStore.getCommittees()});
    });

    this._filesToken = PositionPaperStore.addListener(() => {
      this.setState({files: PositionPaperStore.getPositionPaperFiles()});
    })
  },

  componentWillUnmount() {
    this._countriesToken && this._countriesToken.remove();
    this._committeesToken && this._committeesToken.remove()
    this._assignmentsToken && this._assignmentsToken.remove();
    this._filesToken && this._filesToken.remove();
    this._successTimeout && clearTimeout(this._successTimeout);
  },

  render() {
    if (this.state.current_assignment == null) {
      return (
        <InnerView>
          <form>
            <div className="table-container">
              {this.renderAssignmentList()}
            </div>
          </form>
        </InnerView>
      );
    } else {
      return (
        <InnerView>
          <form>
            <div className="table-container">
              {this.renderRubric()}
            </div>
          </form>
        </InnerView>
      );
    }
  },

  renderRubric() {
    var user = CurrentUserStore.getCurrentUser();
    var paper = this.state.papers[this.state.current_assignment.paper.id];
    var country = this.state.countries[this.state.current_assignment.country];
    var files = this.state.files;
    var rubric = Object.keys(this.state.committees).length ? this.state.committees[user.committee].rubric : null;

    if (rubric != null) {
      return (<PaperGradeTable
              rubric={rubric}
              paper={paper}
              files={files}
              countryName={country.name}
              onChange={this._handleScoreChange}
              onDownload={this._handleDownload}
              onUnset={this._handleUnsetAssignment}
              onSave={this._handleSavePaper}
              loading={this.state.loading}
              success={this.state.success}>
            </PaperGradeTable>);
    } else {
      return <div></div>;
    }
  },

  renderAssignmentList() {
    var assignments = this.state.assignments;
    var countries = this.state.countries;

    if (Object.keys(countries).length) {
        return (<PaperAssignmentList
                  assignments={assignments}
                  countries={countries}
                  onChange={this._handleAssignmentSelect}>
                </PaperAssignmentList>);
    } else {
      return <div></div>;
    }
  },

  _handleScoreChange (field, paperID, event) {
    var paper = this.state.papers[paperID];
    var papers = this.state.papers;
    this.setState({
      papers: {
        ...papers,
        [paperID]: {...paper, [field]: Number(event)},
      },
    });
  },

  _handleUnsetAssignment(event) {
    this.setState({current_assignment: null});
  },

  _handleAssignmentSelect (assignmentID, event) {
    var assignments = this.state.assignments;
    var a = assignments.find(a => a.id == assignmentID);
    this.setState({current_assignment: a});
    PositionPaperActions.fetchPositionPaperFile(a.paper.file, a.paper.id);
  },

  _handleSavePaper(paperID, event) {
    this._successTimout && clearTimeout(this._successTimeout);
    this.setState({loading: true});
    var committee = CurrentUserStore.getCurrentUser().committee;
    var paper = {...this.state.papers[paperID]};
    delete paper['file'];
    paper['graded'] = true;
    PositionPaperActions.updatePositionPaper(
      paper,
      this._handleSuccess,
      this._handleError,
    );
    event.preventDefault();
  },

  _handleSuccess: function(response) {
    this.setState({
      loading: false,
      success: true,
    });

    this._successTimeout = setTimeout(
      () => this.setState({success: false}),
      2000,
    );
  },

  _handleError: function(response) {
    console.log(response);
    this.setState({loading: false});
    window.alert(
      'Something went wrong. Please refresh your page and try again.',
    );
  },
});

module.exports = ChairPapersView;
