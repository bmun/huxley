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
      this.setState({
        files: PositionPaperStore.getPositionPaperFiles(),
        graded_files: PositionPaperStore.getGradedPositionPaperFiles(),
      });
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
    var files = this.state.files;
    var graded_files = this.state.graded_files;
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

        var rows = rubric.use_topic_2 ? '2' : '1';
        var rubric_row_1 = (
          <tr>
            <td rowSpan={rows}>Rubric</td>
            <td rowSpan={rows} />
            <td rowSpan={rows} />
            {rubric.use_topic_2 ? <td>A</td> : null}
            <td>{rubric.grade_value_1}%</td>
            <td>{rubric.grade_value_2}%</td>
            <td>{rubric.grade_value_3}%</td>
            <td>{rubric.grade_value_4}%</td>
            <td>{rubric.grade_value_5}%</td>
            <td>{this.calculateMaxScore(rubric)}%</td>
            <td />
          </tr>
        );
        var rubric_row_2 = rubric.use_topic_2 ? (
          <tr>
            <td>B</td>
            <td>{rubric.grade_t2_value_1}%</td>
            <td>{rubric.grade_t2_value_2}%</td>
            <td>{rubric.grade_t2_value_3}%</td>
            <td>{rubric.grade_t2_value_4}%</td>
            <td>{rubric.grade_t2_value_5}%</td>
            <td>{this.calculateMaxScore(rubric, true)}%</td>
          </tr>
        ) : null;

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
                  <th>Total</th>
                </tr>
              </thead>
              {rubric_row_1}
              {rubric_row_2}
              {this.renderCommitteeRows(
                countryAssignments,
                rubric,
                files,
                graded_files,
                rubric.use_topic_2,
              )}
            </Table>
          </div>
        );
      }.bind(this),
    );
  },

  renderCommitteeRows: function(
    countryAssignments,
    rubric,
    files,
    graded_files,
    topic_2,
  ) {
    return countryAssignments.map(
      function(assignment) {
        var paper =
          assignment.paper && assignment.paper.file ? assignment.paper : null;
        var originalFile = paper
          ? PositionPaperStore.getPositionPaperFile(paper.id)
          : null;
        var gradedFile = paper
          ? PositionPaperStore.getGradedPositionPaperFile(paper.id)
          : null;
        var originalHrefData =
          paper && paper.file && files[assignment.paper.id]
            ? window.URL.createObjectURL(files[assignment.paper.id])
            : null;
        var gradedHrefData =
          paper &&
          paper.graded &&
          paper.graded_file &&
          graded_files[assignment.paper.id]
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
            download={fileName}>
            &#10515;
          </a>
        ) : null;
        var gradedPaper =
          paper && graded ? (
            <a
              className={cx({
                button: true,
                'button-small': true,
                'button-blpaperue': true,
                'rounded-small': true,
              })}
              href={gradedHrefData}
              download={gradedFileName}>
              &#10515;
            </a>
          ) : null;

        var category1 = null;
        var category2 = null;
        var shown1 = null;
        var shown2 = null;
        var shown3 = null;
        var shown4 = null;
        var shown5 = null;
        var shown1_t2 = null;
        var shown2_t2 = null;
        var shown3_t2 = null;
        var shown4_t2 = null;
        var shown5_t2 = null;
        if (paper != null) {
          var score1 = this.calculateTotalScore(paper);
          var maxScore1 = this.calculateMaxScore(rubric);
          var category1 = this.calculateCategory(score1, maxScore1);

          var shown1 = this.calculateCategory(
            paper.score_1,
            rubric.grade_value_1,
          );
          var shown2 = this.calculateCategory(
            paper.score_2,
            rubric.grade_value_2,
          );
          var shown3 = this.calculateCategory(
            paper.score_3,
            rubric.grade_value_3,
          );
          var shown4 = this.calculateCategory(
            paper.score_4,
            rubric.grade_value_4,
          );
          var shown5 = this.calculateCategory(
            paper.score_5,
            rubric.grade_value_5,
          );

          var score2 = this.calculateTotalScore(paper, true);
          var maxScore2 = this.calculateMaxScore(rubric, true);
          var category2 = this.calculateCategory(score2, maxScore2);

          var shown1_t2 = this.calculateCategory(
            paper.score_t2_1,
            rubric.grade_t2_value_1,
          );
          var shown2_t2 = this.calculateCategory(
            paper.score_t2_2,
            rubric.grade_t2_value_2,
          );
          var shown3_t2 = this.calculateCategory(
            paper.score_t2_3,
            rubric.grade_t2_value_3,
          );
          var shown4_t2 = this.calculateCategory(
            paper.score_t2_4,
            rubric.grade_t2_value_4,
          );
          var shown5_t2 = this.calculateCategory(
            paper.score_t2_5,
            rubric.grade_t2_value_5,
          );
        }

        var rows = topic_2 ? '2' : '1';
        var topic_1_row = (
          <tr>
            <td rowSpan={rows}>
              {this.state.countries[assignment.country].name}
            </td>
            <td rowSpan={rows}>{downloadPaper}</td>
            <td rowSpan={rows}>{gradedPaper}</td>
            {topic_2 ? <td>A</td> : null}
            <td>{shown1 && graded ? shown1.substring(0, 1) : null}</td>
            <td>{shown2 && graded ? shown2.substring(0, 1) : null}</td>
            <td>{shown3 && graded ? shown3.substring(0, 1) : null}</td>
            <td>{shown4 && graded ? shown4.substring(0, 1) : null}</td>
            <td>{shown5 && graded ? shown5.substring(0, 1) : null}</td>
            <td>{category1 && graded ? category1 : null}</td>
          </tr>
        );
        var topic_2_row = topic_2 ? (
          <tr>
            <td>B</td>
            <td>{shown1_t2 && graded ? shown1_t2.substring(0, 1) : null}</td>
            <td>{shown2_t2 && graded ? shown2_t2.substring(0, 1) : null}</td>
            <td>{shown3_t2 && graded ? shown3_t2.substring(0, 1) : null}</td>
            <td>{shown4_t2 && graded ? shown4_t2.substring(0, 1) : null}</td>
            <td>{shown5_t2 && graded ? shown5_t2.substring(0, 1) : null}</td>
            <td>{category2 && graded ? category2 : null}</td>
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

  calculateTotalScore: function(paper, topic_2 = false) {
    var totalScore = -1;
    if (topic_2) {
      totalScore =
        paper.score_t2_1 +
        paper.score_t2_2 +
        paper.score_t2_3 +
        paper.score_t2_4 +
        paper.score_t2_5;
    } else {
      totalScore =
        paper.score_1 +
        paper.score_2 +
        paper.score_3 +
        paper.score_4 +
        paper.score_5;
    }
    return totalScore;
  },

  calculateMaxScore: function(rubric, topic_2 = false) {
    var totalMaxScore = -1;
    if (topic_2) {
      totalMaxScore =
        rubric.grade_t2_value_1 +
        rubric.grade_t2_value_2 +
        rubric.grade_t2_value_3 +
        rubric.grade_t2_value_4 +
        rubric.grade_t2_value_5;
    } else {
      totalMaxScore =
        rubric.grade_value_1 +
        rubric.grade_value_2 +
        rubric.grade_value_3 +
        rubric.grade_value_4 +
        rubric.grade_value_5;
    }
    return totalMaxScore;
  },

  calculateCategory: function(value, weight) {
    var interval = weight / 5;
    if (value >= interval * 5) {
      return '5 - Exceeds Expectations';
    } else if (value >= interval * 4) {
      return '4 - Exceeds Expectations';
    } else if (value >= interval * 3) {
      return '3 - Meets Expectations';
    } else if (value >= interval * 2) {
      return '2 - Attempts to Meet Expectations';
    } else if (value >= interval) {
      return '1 - Needs Improvement';
    } else {
      ('0 - Needs Improvement');
    }
  },

  calculateScore: function(category, weight) {
    var interval = weight / 5;
    if (category == '5 - Exceeds Expectations') {
      return interval * 5;
    } else if (category == '4 - Exceeds Expectations') {
      return interval * 4;
    } else if (category == '3 - Meets Expectations') {
      return interval * 3;
    } else if (category == '2 - Attempts to Meet Expectations') {
      return interval * 2;
    } else if (category == '1 - Needs Improvement') {
      return interval;
    } else {
      return 0;
    }
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
