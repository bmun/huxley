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
      var score =
        paper.score_1 +
        paper.score_2 +
        paper.score_3 +
        paper.score_4 +
        paper.score_5 +
        paper.score_t2_1 +
        paper.score_t2_2 +
        paper.score_t2_3 +
        paper.score_t2_4 +
        paper.score_t2_5;
      return (
        <tr key={a.id}>
          <td>{countries[a.country].name}</td>
          <td>{buttonCell}</td>
          <td>{score > 0 ? <div>{score}</div> : <div />}</td>
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

  _handleChange: function(assignmentID, event) {
    this.props.onChange && this.props.onChange(assignmentID, event);
  },
});

module.exports = PaperAssignmentList;
