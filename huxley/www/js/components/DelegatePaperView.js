/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

"use strict";

import React from "react";
import PropTypes from "prop-types";
import history from "utils/history";

var Button = require("components/core/Button");
var {ConferenceContext} = require("components/ConferenceContext");
var CurrentUserStore = require("stores/CurrentUserStore");
var InnerView = require("components/InnerView");
var PaperSubmissionTable = require("components/PaperSubmissionTable");
var PositionPaperActions = require("actions/PositionPaperActions");
var PositionPaperStore = require("stores/PositionPaperStore");
var TextTemplate = require("components/core/TextTemplate");
var User = require("utils/User");
var inflateGrades = require("utils/inflateGrades");

var ServerAPI = require("lib/ServerAPI");

require("css/Table.less");
var DelegatePaperViewText = require("text/DelegatePaperViewText.md");
var DelegatePaperNoSubmissionViewText = require("text/DelegatePaperNoSubmissionViewText.md");

class DelegatePaperView extends React.Component {
  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    PositionPaperActions.storePositionPaper(user.delegate.assignment.paper);
    var papers = PositionPaperStore.getPapers();
    var assignment = user.delegate.assignment;
    if (assignment.paper.file != null) {
      PositionPaperActions.fetchPositionPaperFile(assignment.paper.id);
    }
    var files = PositionPaperStore.getPositionPaperFiles();
    var graded_files = PositionPaperStore.getGradedPositionPaperFiles();

    return {
      papers: papers,
      uploadedFile: null,
      files: files,
      graded_files: graded_files,
      errors: {},
    };
  }

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isDelegate(user)) {
      history.pushState(null, "/");
    }
  }

  componentDidMount() {
    this._papersToken = PositionPaperStore.addListener(() => {
      this.setState({
        files: PositionPaperStore.getPositionPaperFiles(),
        papers: PositionPaperStore.getPapers(),
        graded_files: PositionPaperStore.getGradedPositionPaperFiles(),
      });
    });
  }

  componentWillUnmount() {
    this._papersToken && this._papersToken.remove();
    this._successTimeout && clearTimeout(this._successTimeout);
  }

  render() {
    if (this.context.conference.position_papers_accepted) {
      return (
        <InnerView>
          <div style={{ margin: "auto 20px 20px 20px" }}>
            <TextTemplate>{DelegatePaperViewText}</TextTemplate>
          </div>
          <form>
            <div className="table-container">{this.renderRubric()}</div>
          </form>
        </InnerView>
      );
    } else {
      return (
        <InnerView>
          <div style={{ margin: "auto 20px 20px 20px" }}>
            <TextTemplate>{DelegatePaperNoSubmissionViewText}</TextTemplate>
          </div>
        </InnerView>
      );
    }
  }

  renderRubric() {
    const user = CurrentUserStore.getCurrentUser();
    const paper = this.state.papers[user.delegate.assignment.paper.id];
    const files = this.state.files;
    const graded_file = PositionPaperStore.getGradedPositionPaperFile(paper.id);
    const graded_files = this.state.graded_files;
    const rubric = user.delegate.assignment.committee.rubric;

    if (rubric != null && paper != null) {
      return (
        <PaperSubmissionTable
          rubric={rubric}
          paper={paper}
          files={files}
          graded_files={graded_files}
          onUpload={this._handleUploadPaper}
          onSubmit={this._handleSubmitPaper}
        />
      );
    } else {
      return <div />;
    }
  }
  calculateTotalScore(paper, rubric, topic_2 = false) {
    var totalScore = -1;
    if (topic_2) {
      totalScore =
        inflateGrades(paper.score_t2_1, rubric.grade_t2_value_1) +
        inflateGrades(paper.score_t2_2, rubric.grade_t2_value_2) +
        inflateGrades(paper.score_t2_3, rubric.grade_t2_value_3) +
        inflateGrades(paper.score_t2_4, rubric.grade_t2_value_4) +
        inflateGrades(paper.score_t2_5, rubric.grade_t2_value_5);
    } else {
      totalScore =
        inflateGrades(paper.score_1, rubric.grade_value_1) +
        inflateGrades(paper.score_2, rubric.grade_value_2) +
        inflateGrades(paper.score_3, rubric.grade_value_3) +
        inflateGrades(paper.score_4, rubric.grade_value_4) +
        inflateGrades(paper.score_5, rubric.grade_value_5);
    }
    return totalScore;
  }
  calculateMaxScore(rubric, topic_2 = false) {
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
  }
  calculateCategory(value, weight) {
    var interval = weight / 5;
    if (value >= interval * 5) {
      return "5 - Exceeds Expectations";
    } else if (value >= interval * 4) {
      return "4 - Exceeds Expectations";
    } else if (value >= interval * 3) {
      return "3 - Meets Expectations";
    } else if (value >= interval * 2) {
      return "2 - Attempts to Meet Expectations";
    } else if (value >= interval) {
      return "1 - Needs Improvement";
    } else {
      ("0 - Needs Improvement");
    }
  }
  calculateScore(category, weight) {
    var interval = weight / 5;
    if (category == "5 - Exceeds Expectations") {
      return interval * 5;
    } else if (category == "4 - Exceeds Expectations") {
      return interval * 4;
    } else if (category == "3 - Meets Expectations") {
      return interval * 3;
    } else if (category == "2 - Attempts to Meet Expectations") {
      return interval * 2;
    } else if (category == "1 - Needs Improvement") {
      return interval;
    } else {
      return 0;
    }
  }

  _handleUploadPaper(paperID, event) {
    this.setState({ uploadedFile: event.target.files[0] });
  }

  _handleSubmitPaper(paperID, event) {
    var file = this.state.uploadedFile;
    if (
      file != null &&
      window.confirm(
        `Please make sure this is the file you intend to submit! You have uploaded: ${file.name}.`
      )
    ) {
      var paper = { ...this.state.papers[paperID] };
      paper.file = file.name;

      PositionPaperActions.uploadPaper(
        paper,
        file,
        this._handleSuccess,
        this._handleError
      );

      this.setState({
        uploadedFile: null,
      });
    }
    history.pushState(null, "/");
    event.preventDefault();
  }

  _handleSuccess(response) {
    window.alert("Your paper has been successfully uploaded!");
  }

  _handleError(response) {
    window.alert(
      "Something went wrong. Please refresh your page and try again."
    );
  }
}

DelegatePaperView.contextTypes = {
  conference: PropTypes.shape(ConferenceContext),
};


