/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var Button = require('components/core/Button');

var React = require('react');

var PaperAssignmentList = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    assignments: React.PropTypes.array,
    papers: React.PropTypes.object,
    rubric: React.PropTypes.object,
    countries: React.PropTypes.object,
  },

  render() {
    var assignments = this.props.assignments;
    var countries = this.props.countries;
    var papers = this.props.papers;
    var rows = assignments.map(a => {
      var buttonCell =
        a.paper.file != null ? (
          <Button color="green" onClick={this._handleChange.bind(this, a.id)}>
            Grade
          </Button>
        ) : (
          <div>No paper submitted.</div>
        );

      var paper = papers[a.paper.id];
      var score1 = this.calculateTotalScore(paper);
      var score2 = this.calculateTotalScore(paper, true);
      var maxScore1 = this.calculateMaxScore(this.props.rubric);
      var maxScore2 = this.calculateMaxScore(this.props.rubric, true);
      var category1 = this.calculateCategory(score1, maxScore1);
      var category2 = this.calculateCategory(score2, maxScore2);

      var score = null;
      if (this.props.rubric.use_topic_2) {
        var score = paper.graded ? (
          <div>
            T1:{' '}
            <b>
              {score1} / {maxScore1}
            </b>{' '}
            {category1}
            <br />
            T2:{' '}
            <b>
              {score2} / {maxScore2}
            </b>{' '}
            {category2}
          </div>
        ) : (
          ''
        );
      } else {
        var score = paper.graded ? (
          <div>
            T1:{' '}
            <b>
              {score1} / {maxScore1}
            </b>{' '}
            {category1}
          </div>
        ) : (
          ''
        );
      }

      return (
        <tr key={a.id}>
          <td>{countries[a.country].name}</td>
          <td>{buttonCell}</td>
          <td>{score}</td>
          <td>{a.paper.submission_date}</td>
        </tr>
      );
    });

    return (
      <table>
        <thead>
          <tr>
            <th>Country</th>
            <th />
            <th>Current Score</th>
            <th>Submission Date (PST)</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
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

  _handleChange: function(assignmentID, event) {
    this.props.onChange && this.props.onChange(assignmentID, event);
  },
});

module.exports = PaperAssignmentList;
