/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

"use strict";

import React from "react";
import { history } from "utils/history";

const { CommitteeFeedbackStore } = require("stores/CommitteeFeedbackStore");
const { CurrentUserStore } = require("stores/CurrentUserStore");
const { InnerView } = require("components/InnerView");
const { Table } = require("components/core/Table");
const { TextTemplate } = require("components/core/TextTemplate");
const { User } = require("utils/User");

require("css/Table.less");
const ChairCommitteeFeedbackViewText = require("text/ChairCommitteeFeedbackViewText.md");

class ChairCommitteeFeedbackView extends React.Component {
  constructor(props) {
    super(props);
    var committeeID = CurrentUserStore.getCurrentUser().committee;
    this.state = {
      feedback: CommitteeFeedbackStore.getCommitteeFeedback(committeeID),
    };
  }

  componentDidMount() {
    this._committeeFeedbackToken = CommitteeFeedbackStore.addListener(() => {
      var committeeID = CurrentUserStore.getCurrentUser().committee;
      this.setState({
        feedback: CommitteeFeedbackStore.getCommitteeFeedback(committeeID),
      });
    });
  }

  UNSAFE_componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isChair(user)) {
      history.redirect("/");
    }
  }

  componentsWillUnmount() {
    this._committeeFeedbackToken && this._committeeFeedbackToken.remove();
  }

  render() {
    return (
      <InnerView>
        <TextTemplate>{ChairCommitteeFeedbackViewText}</TextTemplate>
        <div className="table-container">
          <Table
            style={{ margin: "10px auto 0px auto", tableLayout: "auto" }}
            emptyMessage="You have no feedback."
            isEmpty={!this.state.feedback.length}
          >
            <thead>
              <tr>
                <th>Overall Committee Feedback</th>
                {/* <th>Rating</th> */}
              </tr>
            </thead>
            <tbody>{this.renderFeedbackRows(this.state.feedback)}</tbody>
          </Table>
        </div>
        {this.mapFeedbackToTable()}
      </InnerView>
    );
  }

  mapFeedbackToTable = () => {
    var data = {};
    for (var singleFeedback of this.state.feedback) {
      for (var i = 1; i <= 10; i++) {
        var name_key = "chair_" + i + "_name";
        if (singleFeedback[name_key] && singleFeedback[name_key].length) {
          if (!(singleFeedback[name_key] in data)) {
            data[singleFeedback[name_key]] = [];
          }
          var comment_key = "chair_" + i + "_comment";
          var rating_key = "chair_" + i + "_rating";
          if (singleFeedback[comment_key] || singleFeedback[rating_key]) {
            var d = {
              comment: singleFeedback[comment_key],
              rating: singleFeedback[rating_key],
            };
            data[singleFeedback[name_key]].push(d);
          }
          //A Delegate could submit 2 different chair feedbacks for the same name_key
          //It's just another problem with the overall hacky implementation of this
          //that I want to fix anyways
          //So I think for now we just leave it in but mark it as an actual concrete reason
          //of why this needs to be fixed
        }
      }
    }
    var tables = [];

    for (var entry in data) {
      //I'll admit that this is straight up spaghetti code here
      if (data[entry].length) {
        tables.push(
          <div className="table-container">
            <Table
              style={{ margin: "10px auto 0px auto", tableLayout: "auto" }}
              emptyMessage="You have no feedback."
              isEmpty={!this.state.feedback.length}
            >
              <thead>
                <tr>
                  <th>{entry}</th>
                  {/* <th>Rating</th> */}
                </tr>
              </thead>
              <tbody>{this.renderFeedbackRows(data[entry])}</tbody>
            </Table>
          </div>
        );
      }
    }
    return tables;
  };

  renderFeedbackRows = (obj) => {
    return obj.map(function (singleFeedback) {
      return (
        <tr key={singleFeedback.id}>
          <td width={"90%"} style={{whiteSpace:"nowrap"}}>
            {singleFeedback.comment || "No Comment"}
          </td>
          {/* <td>{"No Rating"}</td> */}
        </tr>
      );
    });
  };
}

export { ChairCommitteeFeedbackView };
