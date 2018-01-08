/**
* Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

const React = require('react');
const ReactRouter = require('react-router');

const Button = require('components/core/Button');
const ConferenceContext = require('components/ConferenceContext');
const CurrentUserStore = require('stores/CurrentUserStore');
const CommitteeFeedbackActions = require('actions/CommitteeFeedbackActions');
const CommitteeFeedbackStore = require('stores/CommitteeFeedbackStore');
const InnerView = require('components/InnerView');
const ServerAPI = require('lib/ServerAPI')
const TextTemplate = require('components/core/TextTemplate');
const User = require('utils/User');

const _handleChange = require('utils/_handleChange');

require('css/Table.less');
const DelegateCommitteeFeedbackViewText = require('text/DelegateCommitteeFeedbackViewText.md');

const DelegateCommitteeFeedbackView = React.createClass({

  mixins: [ReactRouter.History],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
  },

  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    var delegate = user.delegate;
    return {
      delegate: delegate,
      comment: "",
      loadingPublish: false,
      feedbackSubmitted: CommitteeFeedbackStore.feedbackSubmitted() || delegate.committee_feedback_submitted,
      errors: {},
    };
  },

  componentDidMount() {
    this._committeeFeedbackToken = CommitteeFeedbackStore.addListener(() => {
      this.setState({
        feedbackSubmitted: CommitteeFeedbackStore.feedbackSubmitted(),
        loadingPublish: false,
      });
    });
  },

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isDelegate(user)) {
      this.history.pushState(null, '/');
    }
  },

  componentWillUnmount(){
    this._committeeFeedbackToken && this._committeeFeedbackToken.remove();
  },

  render() {
    var user = CurrentUserStore.getCurrentUser();
    var delegate = this.state.delegate;
    var assignment = delegate && delegate.assignment;
    var committee = delegate && delegate.assignment.committee;
    var country = delegate && delegate.assignment.country;
    var school = delegate && delegate.school;
    var body = <div />

    if (assignment && school && committee && country) {
      if(this.state.feedbackSubmitted){
        body = (<h3>Thank you for submitting your feedback</h3>);
      } else {
        body = (
        <div>
          <TextTemplate
            firstName={delegate.name}
            conferenceSession={conference.session}
            committee={committee.full_name}>
            {DelegateCommitteeFeedbackViewText}
          </TextTemplate>
          <form>
              <textarea
              className="text-input"
              style={{width: '95%'}}
              rows="6"
              onChange={_handleChange.bind(this,'comment')}
              defaultValue={this.state.feedback}
          />
          <br />
          <br />
          <Button color="green"
            onClick={this._handlePublishFeedback}
            loading={this.state.loadingPublish}
            success={this.state.successPublish}>
            Submit
            </Button>
          </form>
        </div>
        );
      }
    }

    return (
      <InnerView>
        <div style={{textAlign: 'center'}}>
          <br />
          <h2>Committee Feedback</h2>
          <br />
        </div>
        {body}
      </InnerView>
    );
  },

  _handlePublishFeedback(event){
    this.setState({loadingPublish: true});
    var committee_id = this.state.delegate.assignment.committee.id;
    ServerAPI.createCommitteeFeedback(
      {
        comment: this.state.comment,
        committee: committee_id,
      }).then(this._handleAddFeedbackSuccess, this._handleAddFeedbackFail);
    event.preventDefault();
  },

  _handleAddFeedbackSuccess(response){
    CommitteeFeedbackActions.addCommitteeFeedback(response);
  },

  _handleAddFeedbackFail(response){
    this.setState({
      errors: response,
      loading: false,
    });
  }


});

module.exports = DelegateCommitteeFeedbackView;
