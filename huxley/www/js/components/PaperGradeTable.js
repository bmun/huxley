/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var Button = require('components/core/Button');
var NumberInput = require('components/NumberInput');

var cx = require('classnames');
var React = require('react');

var PaperGradeTable = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func,
    onDownload: React.PropTypes.func,
    onUnset: React.PropTypes.func,
    rubric: React.PropTypes.object,
    paper: React.PropTypes.object,
    files: React.PropTypes.object,
    countryName: React.PropTypes.string,
  },

  render() {
    var rubric = this.props.rubric;
    var paper = this.props.paper;
    var files = this.props.files;
    var buttons = <div>
                    <Button
                      color="red"
                      onClick={this._handleUnset}>
                      Go Back
                    </Button>
                  </div>;

    if (paper.id in files) {
      var url = window.URL;
      var hrefData = url.createObjectURL(new Blob([files[paper.id]]));
      var fileNames = paper.file.split('/');
      var fileName = fileNames[fileNames.length-1];
      buttons = <div>
                  <a
                    className={cx({
                                button: true,
                                'button-large': true,
                                'button-green': true,
                                'rounded-small': true,
                              })}
                    href={hrefData}
                    download={fileName}>
                  Download
                  </a>
                  <Button
                    color="red"
                    onClick={this._handleUnset}>
                    Go Back
                  </Button>
                </div>;  
    }

    return (
      <div>
        <table>
          <caption>
            <strong>{this.props.countryName}</strong>
          </caption>
          <thead>
            <tr>
              <th>Category</th>
              <th>Score</th>
              <th>Max Score</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                {rubric.grade_category_1}
              </td>
              <td>
                <label name="session">
                  <NumberInput
                    defaultValue={""+paper.score_1}
                    onChange={this._handleChange.bind(this, "score_1")}
                  />
                </label>
              </td>
              <td>
                {rubric.grade_value_1}
              </td>
            </tr>
            <tr>
              <td>
                {rubric.grade_category_2}
              </td>
              <td>
                <label name="session">
                  <NumberInput
                    defaultValue={""+paper.score_2}
                    onChange={this._handleChange.bind(this, "score_2")}
                  />
                </label>
              </td>
              <td>
                {rubric.grade_value_2}
              </td>
            </tr>
            <tr>
              <td>
                {rubric.grade_category_3}
              </td>
              <td>
                <label name="session">
                  <NumberInput
                    defaultValue={""+paper.score_3}
                    onChange={this._handleChange.bind(this, "score_3")}
                  />
                </label>
              </td>
              <td>
                {rubric.grade_value_3}
              </td>
            </tr>
            <tr>
              <td>
                {rubric.grade_category_4}
              </td>
              <td>
                <label name="session">
                  <NumberInput
                    defaultValue={""+paper.score_4}
                    onChange={this._handleChange.bind(this, "score_4")}
                  />
                </label>
              </td>
              <td>
                {rubric.grade_value_4}
              </td>
            </tr>
            <tr>
              <td>
                {rubric.grade_category_5}
              </td>
              <td>
                <label name="session">
                  <NumberInput
                    defaultValue={""+paper.score_5}
                    onChange={this._handleChange.bind(this, "score_5")}
                  />
                </label>
              </td>
              <td>
                {rubric.grade_value_5}
              </td>
            </tr>
          </tbody>
        </table>
        {buttons}
      </div>
    );
  },

  _handleChange: function(field, event) {
    this.props.onChange &&
      this.props.onChange(field, this.props.paper.id, event);
  },

  _handleDownload: function(event) {
    this.props.onDownload &&
      this.props.onDownload(this.props.paper.id, event);
  },

  _handleUnset: function(event) {
    this.props.onUnset &&
      this.props.onUnset(event);
  }
});

module.exports = PaperGradeTable;
