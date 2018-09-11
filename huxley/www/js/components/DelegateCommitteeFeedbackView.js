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
const ServerAPI = require('lib/ServerAPI');
const SecretariatMemberStore = require('stores/SecretariatMemberStore');
const TextInput = require('components/core/TextInput');
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
    var secretariatMembers = SecretariatMemberStore.getSecretariatMembers(
      delegate.assignment.committee.id,
    );
    return {
      delegate: delegate,
      secretariatMembers: secretariatMembers,
      comment: '',
      rating: 0,
      chair_1_name: '',
      chair_1_comment: '',
      chair_1_rating: 0,
      chair_2_name: '',
      chair_2_comment: '',
      chair_2_rating: 0,
      chair_3_name: '',
      chair_3_comment: '',
      chair_3_rating: 0,
      chair_4_name: '',
      chair_4_comment: '',
      chair_4_rating: 0,
      chair_5_name: '',
      chair_5_comment: '',
      chair_5_rating: 0,
      chair_6_name: '',
      chair_6_comment: '',
      chair_6_rating: 0,
      chair_7_name: '',
      chair_7_comment: '',
      chair_7_rating: 0,
      chair_8_name: '',
      chair_8_comment: '',
      chair_8_rating: 0,
      chair_9_name: '',
      chair_9_comment: '',
      chair_9_rating: 0,
      chair_10_name: '',
      chair_10_comment: '',
      chair_10_rating: 0,
      loadingPublish: false,
      feedbackSubmitted:
        delegate.committee_feedback_submitted ||
        CommitteeFeedbackStore.feedbackSubmitted(),
      errors: {},
    };
  },

  componentDidMount() {
    this._committeeFeedbackToken = CommitteeFeedbackStore.addListener(() => {
      this.setState({
        feedbackSubmitted:
          this.state.feedbackSubmitted ||
          CommitteeFeedbackStore.feedbackSubmitted(),
        loadingPublish: false,
      });
    });

    this._secretariatMembersToken = SecretariatMemberStore.addListener(() => {
      this.setState({
        secretariatMembers: SecretariatMemberStore.getSecretariatMembers(
          this.state.delegate.assignment.committee.id,
        ),
      });
      var newState = {};
      for (var i = 0; i < this.state.secretariatMembers.length; i++) {
        var index = i + 1;
        newState['chair_' + index + '_name'] = this.state.secretariatMembers[
          i
        ].name;
      }
      this.setState(newState);
    });
  },

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isDelegate(user)) {
      this.history.pushState(null, '/');
    }
  },

  componentWillUnmount() {
    this._committeeFeedbackToken && this._committeeFeedbackToken.remove();
    this._secretariatMembersToken && this._secretariatMembersToken.remove();
  },

  render() {
    var user = CurrentUserStore.getCurrentUser();
    var delegate = this.state.delegate;
    var assignment = delegate && delegate.assignment;
    var committee = delegate && delegate.assignment.committee;
    var body = <div />;

    if (assignment && committee) {
      if (this.state.feedbackSubmitted) {
        body = <h3>Thank you for submitting your feedback</h3>;
      } else {
        var head_chair_field;
        var chair_fields = [];
        for (var i = 0; i < this.state.secretariatMembers.length; i++) {
          var index = i + 1;
          var name_key = 'chair_' + index + '_name';
          var comment_key = 'chair_' + index + '_comment';
          var rating_key = 'chair_' + index + '_rating';
          if (this.state.secretariatMembers[i].is_head_chair) {
            head_chair_field = this._buildFeedbackInputs(
              this.state.secretariatMembers[i],
              'Head Chair',
              i + 1,
            );
          } else {
            chair_fields.push(
              this._buildFeedbackInputs(
                this.state.secretariatMembers[i],
                'Vice Chair',
                i + 1,
              ),
            );
          }
        }

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
                onChange={_handleChange.bind(this, 'comment')}
                defaultValue={this.state.feedback}
                placeholder={
                  'General Feedback For ' +
                  this.state.delegate.assignment.committee.name
                }
              />
              <br />
              <label>
                <font size={3}>
                  <b>Rate Committee: </b>
                </font>
                <select
                  onChange={_handleChange.bind(this, 'rating')}
                  value={this.state['rating']}
                  default={0}>
                  <option value={0}>No Rating</option>
                  <option value={10}>10</option>
                  <option value={9}>9</option>
                  <option value={8}>8</option>
                  <option value={7}>7</option>
                  <option value={6}>6</option>
                  <option value={5}>5</option>
                  <option value={4}>4</option>
                  <option value={3}>3</option>
                  <option value={2}>2</option>
                  <option value={1}>1</option>
                </select>
              </label>
              {head_chair_field}
              {chair_fields}
              <br />
              <br />
              <Button
                color="green"
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

  _buildFeedbackInputs(secretariatMember, title, index) {
    var name_key = 'chair_' + index + '_name';
    var comment_key = 'chair_' + index + '_comment';
    var rating_key = 'chair_' + index + '_rating';
    return (
      <div key={index}>
        <br />
        <hr />
        <br />
        <font size={3}>
          <b>
            {title}: {secretariatMember.name}
          </b>
        </font>
        <br />
        <textarea
          className="text-input"
          style={{width: '75%'}}
          rows="4"
          onChange={_handleChange.bind(this, comment_key)}
          defaultValue={this.state[comment_key]}
          placeholder={'Feedback for ' + secretariatMember.name}
        />
        <br />
        <label>
          <font size={3}>
            <b>{'Rate ' + secretariatMember.name + ': '}</b>
          </font>
          <select
            onChange={_handleChange.bind(this, rating_key)}
            value={this.state[rating_key]}
            default={0}>
            <option value={0}>No Rating</option>
            <option value={10}>10</option>
            <option value={9}>9</option>
            <option value={8}>8</option>
            <option value={7}>7</option>
            <option value={6}>6</option>
            <option value={5}>5</option>
            <option value={4}>4</option>
            <option value={3}>3</option>
            <option value={2}>2</option>
            <option value={1}>1</option>
          </select>
        </label>
      </div>
    );
  },

  _handlePublishFeedback(event) {
    this.setState({loadingPublish: true});
    var committee_id = this.state.delegate.assignment.committee.id;
    ServerAPI.createCommitteeFeedback({
      comment: this.state.comment,
      committee: committee_id,
      rating: this.state.rating,
      chair_1_name: this.state.chair_1_name,
      chair_1_rating: this.state.chair_1_rating,
      chair_1_comment: this.state.chair_1_comment,
      chair_2_name: this.state.chair_2_name,
      chair_2_rating: this.state.chair_2_rating,
      chair_2_comment: this.state.chair_2_comment,
      chair_3_name: this.state.chair_3_name,
      chair_3_rating: this.state.chair_3_rating,
      chair_3_comment: this.state.chair_3_comment,
      chair_4_name: this.state.chair_4_name,
      chair_4_rating: this.state.chair_4_rating,
      chair_4_comment: this.state.chair_4_comment,
      chair_5_name: this.state.chair_5_name,
      chair_5_rating: this.state.chair_5_rating,
      chair_5_comment: this.state.chair_5_comment,
      chair_6_name: this.state.chair_6_name,
      chair_6_rating: this.state.chair_6_rating,
      chair_6_comment: this.state.chair_6_comment,
      chair_7_name: this.state.chair_7_name,
      chair_7_rating: this.state.chair_7_rating,
      chair_7_comment: this.state.chair_7_comment,
      chair_8_name: this.state.chair_8_name,
      chair_8_rating: this.state.chair_8_rating,
      chair_8_comment: this.state.chair_8_comment,
      chair_9_name: this.state.chair_9_name,
      chair_9_rating: this.state.chair_9_rating,
      chair_9_comment: this.state.chair_9_comment,
      chair_10_name: this.state.chair_10_name,
      chair_10_rating: this.state.chair_10_rating,
      chair_10_comment: this.state.chair_10_comment,
    }).then(this._handleAddFeedbackSuccess, this._handleAddFeedbackFail);
    event.preventDefault();
  },

  _handleAddFeedbackSuccess(response) {
    CommitteeFeedbackActions.addCommitteeFeedback(response);
  },

  _handleAddFeedbackFail(response) {
    this.setState({
      errors: response,
      loading: false,
    });
  },
});

module.exports = DelegateCommitteeFeedbackView;
