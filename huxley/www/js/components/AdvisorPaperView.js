/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var _accessSafe = require('utils/_accessSafe');
var AssignmentStore = require('stores/AssignmentStore');
var Button = require('components/core/Button');
var CommitteeStore = require('stores/CommitteeStore');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var ConferenceContext = require('components/ConferenceContext');
var InnerView = require('components/InnerView');
var PositionPaperStore = require('stores/PositionPaperStore');
var RubricStore = require('stores/RubricStore');
var ServerAPI = require('lib/ServerAPI');
var StatusLabel = require('components/core/StatusLabel');
var Table = require('components/core/Table');
var TextTemplate = require('components/core/TextTemplate');
var _checkDate = require('utils/_checkDate');
var _handleChange = require('utils/_handleChange');

const cx = require('classnames');
var AdvisorPaperViewText = require('text/AdvisorPaperViewText.md');
var AdvisorWaitlistText = require('text/AdvisorWaitlistText.md');

var AdvisorPaperView = React.createClass({
  mixins: [ReactRouter.History],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
  },

  getInitialState: function() {
    var schoolID = CurrentUserStore.getCurrentUser().school.id;
    var conferenceID = this.context.conference.session;
    return {
      assignments: AssignmentStore.getSchoolAssignments(schoolID),
      committees: CommitteeStore.getCommittees(),
      countries: CountryStore.getCountries(),
      files: PositionPaperStore.getPositionPaperFiles(),
      graded_files: PositionPaperStore.getGradedPositionPaperFiles(),
      rubric: RubricStore.getRubric,
      loading: false,
      errors: {},
    };
  },

  componentDidMount: function() {
    var schoolID = CurrentUserStore.getCurrentUser().school.id;
    var conferenceID = this.context.conference.session;
    this._committeesToken = CommitteeStore.addListener(() => {
      this.setState({
        committees: CommitteeStore.getCommittees(),
      });
    });
    this._countriesToken = CountryStore.addListener(() => {
      this.setState({
        countries: CountryStore.getCountries(),
      });
    });
    this._assignmentsToken = AssignmentStore.addListener(() => {
      var assignments = AssignmentStore.getSchoolAssignments(schoolID).filter(
        assignment => !assignment.rejected,
      );
      var assignment_ids = {};
      assignments.map(
        function(a) {
          assignment_ids[a.id] = a;
        }.bind(this),
      );
      this.setState({
        assignments: assignments,
        assignment_ids: assignment_ids,
      });
    });
    this._papersToken = PositionPaperStore.addListener(() => {
      this.setState({files: PositionPaperStore.getPositionPaperFiles(),
        graded_files: PositionPaperStore.getGradedPositionPaperFiles(),});
    });
    this._rubricsToken = RubricStore.addListener(() => {
      this.setState({
        rubric: RubricStore.getRubric,
      });
    });
  },

  componentWillUnmount: function() {
    this._registrationToken && this._registrationToken.remove();
    this._rubricsToken && this._rubricsToken.remove();
    this._papersToken && this._papersToken.remove();
    this._countriesToken && this._countriesToken.remove();
    this._committeesToken && this._committeesToken.remove();
    this._assignmentsToken && this._assignmentsToken.remove();
  },

  render: function() {
    var conference = this.context.conference;
    var registration = this.state.registration;
    var waitlisted =
      _accessSafe(registration, 'is_waitlisted') == null
        ? null
        : registration.is_waitlisted;
    var disableEdit = _checkDate();

    if (waitlisted) {
      return (
        <InnerView>
          <TextTemplate
            conferenceSession={conference.session}
            conferenceExternal={conference.external}>
            {AdvisorWaitlistText}
          </TextTemplate>
        </InnerView>
      );
    } else {
      return (
        <InnerView>
          <TextTemplate>{AdvisorPaperViewText}</TextTemplate>
          {this.renderPaperTables()}
        </InnerView>
      );
    }
  },

  renderPaperTables: function() {
    var committees = {};
    var cm = this.state.committees;
    var countries = this.state.countries;
    var assignments = this.state.assignments;
    var get_rubric = this.state.rubric;
    this.state.assignments.map(
      function(a) {
        var current_committee = cm[a.committee] ? cm[a.committee].name : null;
        if (current_committee) {
          committees[current_committee] =
            committees[current_committee] == undefined
              ? [a]
              : committees[current_committee].concat([a]);
        }
      }.bind(this),
    );

    return Object.keys(committees).map(
      function(c) {
        var countryAssignments = committees[c];
        var committee = cm[countryAssignments[0].committee];
        var rubric = committee.rubric;
        return (
          <div>
            <h4>{committee.name}</h4>
            <Table
              emptyMessage="You don't have any assignments."
              isEmpty={!assignments.length}>
              <thead>
                <tr>
                  <th width="13%">Assignment</th>
                  <th width="12%">Submitted</th>
                  <th width="10.5%">Graded</th>
                  {rubric.use_topic_2 ? <th width="7%">Topic</th> : null}
                  <th width="11.5%">Category 1</th>
                  <th width="11.5%">Category 2</th>
                  <th width="11.5%">Category 3</th>
                  <th width="11.5%">Category 4</th>
                  <th width="11.5%">Category 5</th>
                </tr>
              </thead>
              {this.renderCommitteeRows(
                countryAssignments,
                rubric,
                rubric.use_topic_2,
              )}
            </Table>
          </div>
        );
      }.bind(this),
    );
  },

  renderCommitteeRows: function(countryAssignments, rubric, topic_2) {
    return countryAssignments.map(
      function(assignment) {
        var paper =
          assignment.paper && assignment.paper.file ? assignment.paper : null;
        var originalHrefData =
          paper && paper.file && files[assignment.paper.id]
            ? window.URL.createObjectURL(files[assignment.paper.id])
            : null;
        var gradedHrefData =
          paper && paper.graded && paper.graded_file && graded_files[assignment.paper.id]
            ? window.URL.createObjectURL(graded_files[assignment.paper.id])
            : null;
        var names = paper ? paper.file.split('/') : null;
        var graded = assignment.paper.graded;
        var fileName = names ? names[names.length - 1] : null;
        var gradedFileName = fileName ? 'graded_' + fileName : null;
        var downloadPaper = paper ? (
          <a
            className={cx({
              button: true,
              'button-small': true,
              'button-green': true,
              'rounded-small': true,
            })}
            href={originalHrefData}
            download={assignment.paper.file}>
            &#10515;
          </a>
        ) : null;
        var gradedPaper =
          paper && graded ? (
            <a
              className={cx({
                button: true,
                'button-small': true,
                'button-blue': true,
                'rounded-small': true,
              })}
              href={gradedHrefData}
              download={assignment.paper.graded_file}>
              &#10515;
            </a>
          ) : null;
        var rows = topic_2 ? '2' : '1';
        var topic_1_row = (
          <tr>
            <td rowSpan={rows}>
              {this.state.countries[assignment.country].name}
            </td>
            <td rowSpan={rows}>{downloadPaper}</td>
            <td rowSpan={rows}>{gradedPaper}</td>
            {topic_2 ? <td>A</td> : null}
            <td>{graded ? assignment.paper.score_1 : null}</td>
            <td>{graded ? assignment.paper.score_2 : null}</td>
            <td>{graded ? assignment.paper.score_3 : null}</td>
            <td>{graded ? assignment.paper.score_4 : null}</td>
            <td>{graded ? assignment.paper.score_5 : null}</td>
          </tr>
        );
        var topic_2_row = topic_2 ? (
          <tr>
            <td>B</td>
            <td>{graded ? assignment.paper.score_t2_1 : null}</td>
            <td>{graded ? assignment.paper.score_t2_2 : null}</td>
            <td>{graded ? assignment.paper.score_t2_3 : null}</td>
            <td>{graded ? assignment.paper.score_t2_4 : null}</td>
            <td>{graded ? assignment.paper.score_t2_5 : null}</td>
          </tr>
        ) : null;
        return (
          <tbody>
            {topic_1_row}
            {topic_2_row}
          </tbody>
        );
      }.bind(this),
    );
  },

  renderError: function(field) {
    if (this.state.errors[field]) {
      return (
        <StatusLabel status="error">{this.state.errors[field]}</StatusLabel>
      );
    }

    return null;
  },

  _handleError: function(response) {
    this.setState({
      errors: response,
      loading: false,
    });
  },
});

module.exports = AdvisorPaperView;
