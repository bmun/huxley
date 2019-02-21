/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

const Button = require('components/core/Button');
const NumberInput = require('components/NumberInput');
const TextTemplate = require('components/core/TextTemplate');

const PaperGradeText = require('text/PaperGradeText.md');

const cx = require('classnames');
const React = require('react');

const PaperGradeTable = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    onDownload: React.PropTypes.func,
    onUnset: React.PropTypes.func,
    onSave: React.PropTypes.func,
    onUpload: React.PropTypes.func,
    onSubmit: React.PropTypes.func,
    rubric: React.PropTypes.object,
    paper: React.PropTypes.object,
    files: React.PropTypes.object,
    graded_files: React.PropTypes.object,
    countryName: React.PropTypes.string,
    loading: React.PropTypes.bool,
    success: React.PropTypes.bool,
  },

  render() {
    const rubric = this.props.rubric;
    const paper = this.props.paper;
    const files = this.props.files;
    const graded_files = this.props.graded_files;
    var buttons = (
      <div>
        <Button color="red" onClick={this._handleUnset}>
          Go Back
        </Button>
        <div>Waiting to receive file from server...</div>
      </div>
    );

    if (paper.id in files) {
      var url = window.URL;
      var hrefData = url.createObjectURL(files[paper.id]);
      var gradedHrefData =
        graded_files[paper.id] && paper.graded
          ? url.createObjectURL(graded_files[paper.id])
          : null;
      var fileNames = paper.file.split('/');
      var fileName = fileNames[fileNames.length - 1];
      var gradedName = gradedHrefData ? 'graded_' + fileName : null;
      var downloadGraded = gradedHrefData ? (
        <a
          className={cx({
            button: true,
            'button-large': true,
            'button-green': true,
            'rounded-small': true,
          })}
          href={gradedHrefData}
          download={gradedName}>
          Download Graded
        </a>
      ) : null;
      buttons = (
        <div>
          <Button color="red" onClick={this._handleUnset}>
            Go Back
          </Button>
          <a
            className={cx({
              button: true,
              'button-large': true,
              'button-green': true,
              'rounded-small': true,
            })}
            href={hrefData}
            download={fileName}>
            Download Original
          </a>
          {downloadGraded}
          <Button
            color="blue"
            onClick={this._handleSave}
            loading={this.props.loading}
            success={this.props.success}>
            Submit
          </Button>
        </div>
      );
    }

    var secondRubric = rubric.use_topic_2 ? (
      this._renderTopicTwo(rubric, paper)
    ) : (
      <tbody />
    );

    return (
      <div>
        <table>
          <caption>
            <strong>{this.props.countryName}</strong>
            <TextTemplate>{PaperGradeText}</TextTemplate>
          </caption>
          <thead>
            <tr>
              <th>Category</th>
              <th>Score</th>
              <th>Weight</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Topic: &ensp; {rubric.topic_one}</td>
            </tr>
            <tr>
              <td>{rubric.grade_category_1}</td>
              <td>
                {this.renderDropdown(
                  'score_1',
                  paper.score_1,
                  rubric.grade_value_1,
                )}
              </td>
              <td>{rubric.grade_value_1}</td>
            </tr>
            <tr>
              <td>{rubric.grade_category_2}</td>
              <td>
                {this.renderDropdown(
                  'score_2',
                  paper.score_2,
                  rubric.grade_value_2,
                )}
              </td>
              <td>{rubric.grade_value_2}</td>
            </tr>
            <tr>
              <td>{rubric.grade_category_3}</td>
              <td>
                {this.renderDropdown(
                  'score_3',
                  paper.score_3,
                  rubric.grade_value_3,
                )}
              </td>
              <td>{rubric.grade_value_3}</td>
            </tr>
            <tr>
              <td>{rubric.grade_category_4}</td>
              <td>
                {this.renderDropdown(
                  'score_4',
                  paper.score_4,
                  rubric.grade_value_4,
                )}
              </td>
              <td>{rubric.grade_value_4}</td>
            </tr>
            <tr>
              <td>{rubric.grade_category_5}</td>
              <td>
                {this.renderDropdown(
                  'score_5',
                  paper.score_5,
                  rubric.grade_value_5,
                )}
              </td>
              <td>{rubric.grade_value_5}</td>
            </tr>
          </tbody>
          {secondRubric}
          <tbody>
            <tr>
              <td>Upload Graded Paper:</td>
              <td>
                <div>
                  <input
                    type="file"
                    accept=".doc, .docx, .pdf, application/pdf, application/ms-word, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    onChange={this._handleUpload}
                  />
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        {buttons}
      </div>
    );
  },

  _renderTopicTwo: function(rubric, paper) {
    return (
      <tbody>
        <tr>
          <td>Topic: &ensp; {rubric.topic_two}</td>
        </tr>
        <tr>
          <td>{rubric.grade_t2_category_1}</td>
          <td>
            {this.renderDropdown(
              'score_t2_1',
              paper.score_t2_1,
              rubric.grade_t2_value_1,
            )}
          </td>
          <td>{rubric.grade_t2_value_1}</td>
        </tr>
        <tr>
          <td>{rubric.grade_t2_category_2}</td>
          <td>
            {this.renderDropdown(
              'score_t2_2',
              paper.score_t2_2,
              rubric.grade_t2_value_2,
            )}
          </td>
          <td>{rubric.grade_t2_value_2}</td>
        </tr>
        <tr>
          <td>{rubric.grade_t2_category_3}</td>
          <td>
            {this.renderDropdown(
              'score_t2_3',
              paper.score_t2_3,
              rubric.grade_t2_value_3,
            )}
          </td>
          <td>{rubric.grade_t2_value_3}</td>
        </tr>
        <tr>
          <td>{rubric.grade_t2_category_4}</td>
          <td>
            {this.renderDropdown(
              'score_t2_4',
              paper.score_t2_4,
              rubric.grade_t2_value_4,
            )}
          </td>
          <td>{rubric.grade_t2_value_4}</td>
        </tr>
        <tr>
          <td>{rubric.grade_t2_category_5}</td>
          <td>
            {this.renderDropdown(
              'score_t2_5',
              paper.score_t2_5,
              rubric.grade_t2_value_5,
            )}
          </td>
          <td>{rubric.grade_t2_value_5}</td>
        </tr>
      </tbody>
    );
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
      ('0 - Missing Section');
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

  renderDropdown: function(name, score, max_score) {
    var interval = this.calculateCategory(score, max_score);
    return (
      <select
        onChange={this._handleDropdownChange.bind(this, name, max_score)}
        value={interval}>
        <option key={'0 - Missing Section'} value={'0 - Missing Section'}>
          0 - Missing Section
        </option>
        <option
          key={'5 - Exceeds Expectations'}
          value={'5 - Exceeds Expectations'}>
          5 - Exceeds Expectations
        </option>
        <option
          key={'4 - Exceeds Expectations'}
          value={'4 - Exceeds Expectations'}>
          4 - Exceeds Expectations
        </option>
        <option key={'3 - Meets Expectations'} value={'3 - Meets Expectations'}>
          3 - Meets Expectations
        </option>
        <option
          key={'2 - Attempts to Meet Expectations'}
          value={'2 - Attempts to Meet Expectations'}>
          2 - Attempts to Meet Expectations
        </option>
        <option key={'1 - Needs Improvement'} value={'1 - Needs Improvement'}>
          1 - Needs Improvement
        </option>
      </select>
    );
  },

  _handleDropdownChange: function(field, max_score, event) {
    var new_score = this.calculateScore(event.target.value, max_score);
    this.props.onChange &&
      this.props.onChange(field, this.props.paper.id, new_score);
  },

  _handleChange: function(field, event) {
    this.props.onChange &&
      this.props.onChange(field, this.props.paper.id, event);
  },

  _handleUnset: function(event) {
    this.props.onUnset && this.props.onUnset(event);
  },

  _handleSave: function(event) {
    this.props.onSave && this.props.onSave(this.props.paper.id, event);
  },

  _handleUpload: function(event) {
    this.props.onUpload && this.props.onUpload(this.props.paper.id, event);
  },

  _handleSubmit: function(event) {
    this.props.onSubmit && this.props.onSubmit(this.props.paper.id, event);
  },
});

module.exports = PaperGradeTable;
