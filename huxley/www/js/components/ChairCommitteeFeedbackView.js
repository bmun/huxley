/**
* Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var CommitteeFeedbackStore = require('stores/CommitteeFeedbackStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var InnerView = require('components/InnerView');
var TextTemplate = require('components/core/TextTemplate');
var User = require('utils/User');

require('css/Table.less');
var ChairCommitteeFeedbackViewText = require('text/ChairCommitteeFeedbackViewText.md');

var ChairCommitteeFeedbackView = React.createClass({
  mixins: [ReactRouter.History],

  getInitialState() {
    var committeeID = CurrentUserStore.getCurrentUser().committee;
    return {
      feedback: CommitteeFeedbackStore.getCommitteeFeedback(committeeID),
    };
  },

  componentDidMount() {
    this._committeeFeedbackToken = CommitteeFeedbackStore.addListener(() => {
      var committeeID = CurrentUserStore.getCurrentUser().committee;
      this.setState({
        feedback: CommitteeFeedbackStore.getCommitteeFeedback(committeeID),
      });
    });
  },

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isChair(user)) {
      this.history.pushState(null, '/');
    }
  },

  componentsWillUnmount() {
    this._committeeFeedbackToken && this._committeeFeedbackToken.remove();
  },

  render() {
    return (
      <InnerView>
        <TextTemplate>
          {ChairCommitteeFeedbackViewText}
        </TextTemplate>
        <div className="table-container">
          <table
            style={{margin: '10px auto 0px auto'}}
            emptyMessage="You have no feedback."
            isEmpty={!this.state.feedback.length}>
            <thead>
              <tr>
                <th>Feedback</th>
              </tr>
            </thead>
            <tbody>
              {this.renderFeedbackRows()}
            </tbody>
          </table>
        </div>
      </InnerView>
    );
  },

  renderFeedbackRows() {
    return this.state.feedback.map(function(singleFeedback) {
      return (
        <tr>
          <td>
            {singleFeedback.comment}
          </td>
        </tr>
      );
    });
  },
});

module.exports = ChairCommitteeFeedbackView;
