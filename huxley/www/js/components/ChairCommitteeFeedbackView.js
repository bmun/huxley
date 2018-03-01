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
        <TextTemplate>{ChairCommitteeFeedbackViewText}</TextTemplate>
        <div className="table-container">
          <table
            style={{margin: '10px auto 0px auto', tableLayout: 'auto'}}
            emptyMessage="You have no feedback."
            isEmpty={!this.state.feedback.length}>
            <thead>
              <tr>
                <th>Overall Committee Feedback</th>
                <th>Rating</th>
              </tr>
            </thead>
            <tbody>{this.renderFeedbackRows(this.state.feedback)}</tbody>
          </table>
        </div>
        {this.mapFeedbackToTable()}
      </InnerView>
    );
  },

  mapFeedbackToTable() {
    var data = {};
    for (var singleFeedback of this.state.feedback) {
      for (var i = 1; i <= 10; i++) {
        var name_key = 'chair_' + i + '_name';
        if (singleFeedback[name_key] && singleFeedback[name_key].length) {
          if (!(singleFeedback[name_key] in data)) {
            data[singleFeedback[name_key]] = [];
          }
          var comment_key = 'chair_' + i + '_comment';
          var rating_key = 'chair_' + i + '_rating';
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
            <table
              style={{margin: '10px auto 0px auto', tableLayout: 'auto'}}
              emptyMessage="You have no feedback."
              isEmpty={!this.state.feedback.length}>
              <thead>
                <tr>
                  <th>{entry}</th>
                  <th>Rating</th>
                </tr>
              </thead>
              <tbody>{this.renderFeedbackRows(data[entry])}</tbody>
            </table>
          </div>,
        );
      }
    }
    return tables;
  },

  renderFeedbackRows(obj) {
    return obj.map(function(singleFeedback) {
      return (
        <tr>
          <td width={'90%'} nowrap>
            {singleFeedback.comment || 'No Comment'}
          </td>
          <td>{singleFeedback.rating || 'No Rating'}</td>
        </tr>
      );
    });
  },
});

module.exports = ChairCommitteeFeedbackView;
