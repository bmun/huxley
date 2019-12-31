/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var Button = require('components/core/Button');
var NumberInput = require('components/NumberInput');

var cx = require('classnames');
var React = require('react');

var PaperSubmissionTable = React.createClass({
  propTypes: {
    onUpload: React.PropTypes.func,
    onSubmit: React.PropTypes.func,
    rubric: React.PropTypes.object,
    paper: React.PropTypes.object,
    files: React.PropTypes.object,
    graded_files: React.PropTypes.object,
  },

  render() {
    var rubric = this.props.rubric;
    var paper = this.props.paper;
    var files = this.props.files;
    var graded_files = this.props.graded_files;
    var buttons = <div />;

    if (paper.id in files) {
      var url = window.URL;
      var hrefData = files[paper.id]
        ? url.createObjectURL(files[paper.id])
        : null;
      var gradedHrefData = graded_files[paper.id]
        ? url.createObjectURL(graded_files[paper.id])
        : null;
      var fileNames = paper.file.split('/');
      var fileName = fileNames[fileNames.length - 1];
      var gradedButton = paper.graded ? (
        <a
          className={cx({
            button: true,
            'button-large': true,
            'button-blue': true,
            'rounded-small': true,
          })}
          href={gradedHrefData}
          download={'graded_' + fileName}>
          Download Graded Paper
        </a>
      ) : null;
      buttons = (
        <div>
          <a
            className={cx({
              button: true,
              'button-large': true,
              'button-green': true,
              'rounded-small': true,
            })}
            href={hrefData}
            download={fileName}>
            Download Paper
          </a>
          {gradedButton}
        </div>
      );
    }

    if (!paper.graded) {
      return (
        <div>
          <table>
            <tbody>
              <tr>
                <td>Upload Paper:</td>
                <td>
                  <div>
                    <input
                      type="file"
                      accept=".doc, .docx, .pdf, application/pdf, application/ms-word, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                      onChange={this._handleUpload}
                    />
                    <input type="submit" onClick={this._handleSubmit} />
                  </div>
                </td>
              </tr>
              <tr>
                <td>Uploaded file:</td>
                <td>{buttons}</td>
              </tr>
            </tbody>
          </table>
        </div>
      );
    }

    var secondRuric = rubric.use_topic_2 ? (
      this._renderTopicTwo(rubric, paper)
    ) : (
      <tbody />
    );

    var paper = this.props.paper;
    var rubric = this.props.rubric;

    var score1 = this.calculateTotalScore(paper);
    var maxScore1 = this.calculateMaxScore(rubric);
    var category1 = this.calculateCategory(score1, maxScore1);

    return (
      <div>
        <table>
          <thead>
            <tr>
              <th>Topic</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{rubric.topic_one} </td>
              <td>
                <b>{category1}</b>
              </td>
            </tr>
          </tbody>
          {secondRuric}
        </table>
        {buttons}
      </div>
    );
  },

  _renderTopicTwo: function(rubric, paper) {
    var paper = this.props.paper;
    var rubric = this.props.rubric;
    var score2 = this.calculateTotalScore(paper, true);
    var maxScore2 = this.calculateMaxScore(rubric, true);
    var category2 = this.calculateCategory(score2, maxScore2);

    return (
      <tbody>
        <tr>
          <td>{rubric.topic_two}</td>
          <td>
            <b>{category2}</b>
          </td>
        </tr>
      </tbody>
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

  _handleUpload: function(event) {
    this.props.onUpload && this.props.onUpload(this.props.paper.id, event);
  },

  _handleSubmit: function(event) {
    this.props.onSubmit && this.props.onSubmit(this.props.paper.id, event);
  },
});

module.exports = PaperSubmissionTable;
