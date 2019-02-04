/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var Modal = require('react-modal');
var React = require('react');
var ReactRouter = require('react-router');

var _accessSafe = require('utils/_accessSafe');
var AssignmentActions = require('actions/AssignmentActions');
var AssignmentStore = require('stores/AssignmentStore');
var Button = require('components/core/Button');
var CommitteeStore = require('stores/CommitteeStore');
var CountryStore = require('stores/CountryStore');
var CurrentUserStore = require('stores/CurrentUserStore');
var DelegateActions = require('actions/DelegateActions');
var DelegateStore = require('stores/DelegateStore');
var ConferenceContext = require('components/ConferenceContext');
var CurrentUserActions = require('actions/CurrentUserActions');
var InnerView = require('components/InnerView');
var RegistrationStore = require('stores/RegistrationStore');
var RubricStore = require('stores/RubricStore');
var ServerAPI = require('lib/ServerAPI');
var StatusLabel = require('components/core/StatusLabel');
var Table = require('components/core/Table');
var TextInput = require('components/core/TextInput');
var TextTemplate = require('components/core/TextTemplate');
var _checkDate = require('utils/_checkDate');
var _handleChange = require('utils/_handleChange');

require('css/Modal.less');
var AdvisorRosterViewText = require('text/AdvisorRosterViewText.md');
var AdvisorPaperViewText = require('text/AdvisorPaperViewText.md');
var AdvisorWaitlistText = require('text/AdvisorWaitlistText.md');

var AdvisorPaperView = React.createClass({
  mixins: [ReactRouter.History],

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext),
  },

  getInitialState: function() {
    var schoolID = CurrentUserStore.getCurrentUser().school.id;
    var conferenceID = this.context.conference.session;
    return {
      delegates: DelegateStore.getSchoolDelegates(schoolID),
      registration: RegistrationStore.getRegistration(schoolID, conferenceID),
      assignments: AssignmentStore.getSchoolAssignments(schoolID),
      committees: CommitteeStore.getCommittees(),
      countries: CountryStore.getCountries(),
      loading: false,
      modal_open: false,
      modal_name: '',
      modal_email: '',
      modal_onClick: null,
      errors: {},
    };
  },

  componentWillMount: function() {
    Modal.setAppElement('body');
  },

  componentDidMount: function() {
    var schoolID = CurrentUserStore.getCurrentUser().school.id;
    var conferenceID = this.context.conference.session;
    this._registrationToken = RegistrationStore.addListener(() => {
      this.setState({
        registration: RegistrationStore.getRegistration(schoolID, conferenceID),
      });
    });
    this._delegatesToken = DelegateStore.addListener(() => {
      this.setState({
        registration: RegistrationStore.getRegistration(schoolID, conferenceID),
        delegates: DelegateStore.getSchoolDelegates(schoolID),
        modal_open: false,
        loading: false,
      });
    });
  },

  componentWillUnmount: function() {
    this._registrationToken && this._registrationToken.remove();
    this._delegatesToken && this._delegatesToken.remove();
  },

  render: function() {
    var conference = this.context.conference;
    var registration = this.state.registration;
    var waitlisted =
      _accessSafe(registration, 'is_waitlisted') == null
        ? null
        : registration.is_waitlisted;
    var disableEdit = _checkDate();

    if (waitlisted) {
      return (
        <InnerView>
          <TextTemplate
            conferenceSession={conference.session}
            conferenceExternal={conference.external}>
            {AdvisorWaitlistText}
          </TextTemplate>
        </InnerView>
      );
    } else {
      return (
        <InnerView>
          <TextTemplate>{AdvisorPaperViewText}</TextTemplate>
          {this.renderPaperTables()}
        </InnerView>
      );
    }
  },

  renderPaperTables: function() {
    var committees = {};
    var cm = this.state.committees;
    var countries = this.state.countries;
    var assignments = this.state.assignments;
    var rubrics = this.state.rubrics;
    this.state.assignments.map(
      function(a) {
        var current_committee = cm[a.committee].name;
        committees[current_committee] =
          committees[current_committee] == undefined
            ? [a]
            : committees[current_committee].concat([a]);
        console.log(committees);
      }.bind(this),
    );

    return Object.keys(committees).map(function(c) {
      var countryAssignments = committees[c];
      var committee = cm[countryAssignments[0].committee];
      var rubric = RubricStore.getRubric(committee.rubric);
      if (rubric.use_topic_2) {
        return (
          <Table
            emptyMessage="You don't have any delegates in your roster."
            isEmpty={!this.state.delegates.length}>
            <thead>
              <tr>
                <th>Assignment</th>
                <th>Position Paper</th>
                <th>Graded</th>
                <th>Delete</th>
                <th>{rubric.grade_category_1}</th>
                <th>{rubric.grade_category_2}</th>
                <th>{rubric.grade_category_3}</th>
                <th>{rubric.grade_category_4}</th>
                <th>{rubric.grade_category_5}</th>
                <th>{rubric.grade_t2_category_1}</th>
                <th>{rubric.grade_t2_category_2}</th>
                <th>{rubric.grade_t2_category_3}</th>
                <th>{rubric.grade_t2_category_4}</th>
                <th>{rubric.grade_t2_category_5}</th>
              </tr>
            </thead>
            <tbody>{renderCommitteeRows(countryAssignments, true)}</tbody>
          </Table>
        );
      } else {
        return (
          <Table
            emptyMessage="You don't have any delegates in your roster."
            isEmpty={!this.state.delegates.length}>
            <thead>
              <tr>
                <th>Assignment</th>
                <th>Position Paper</th>
                <th>Graded</th>
                <th>Delete</th>
                <th>{rubric.grade_category_1}</th>
                <th>{rubric.grade_category_2}</th>
                <th>{rubric.grade_category_3}</th>
                <th>{rubric.grade_category_4}</th>
                <th>{rubric.grade_category_5}</th>
              </tr>
            </thead>
            <tbody>{renderCommitteeRows(countryAssignments, false)}</tbody>
          </Table>
        );
      }
    });
  },

  renderCommitteeRows: function(countryAssignments, topic_2) {
    if (!topic_2) {
      return countryAssignments.map(function(assignment) {
        return (
          <tr>
            <td>{assignment.country}</td>
            <td>
              <a
                className={cx({
                  button: true,
                  'button-large': true,
                  'button-green': true,
                  'rounded-small': true,
                })}
                href={hrefData}
                download={assignment.paper.file}>
                Download Paper
              </a>
            </td>
            <td>
              <a
                className={cx({
                  button: true,
                  'button-large': true,
                  'button-green': true,
                  'rounded-small': true,
                })}
                href={hrefData}
                download={assignment.paper.file}>
                Download Paper
              </a>
            </td>
            <td>{assignment.paper.score_1}</td>
            <td>{assignment.paper.score_2}</td>
            <td>{assignment.paper.score_3}</td>
            <td>{assignment.paper.score_4}</td>
            <td>{assignment.paper.score_5}</td>
          </tr>
        );
      });
    } else {
      return countryAssignments.map(function(assignment) {
        return (
          <tr>
            <td>{assignment.country}</td>
            <td>
              <a
                className={cx({
                  button: true,
                  'button-large': true,
                  'button-green': true,
                  'rounded-small': true,
                })}
                href={hrefData}
                download={assignment.paper.file}>
                Download Paper
              </a>
            </td>
            <td>
              <a
                className={cx({
                  button: true,
                  'button-large': true,
                  'button-green': true,
                  'rounded-small': true,
                })}
                href={hrefData}
                download={assignment.paper.file}>
                Download Paper
              </a>
            </td>
            <td>{assignment.paper.score_1}</td>
            <td>{assignment.paper.score_2}</td>
            <td>{assignment.paper.score_3}</td>
            <td>{assignment.paper.score_4}</td>
            <td>{assignment.paper.score_5}</td>
            <td>{assignment.paper.score_t2_1}</td>
            <td>{assignment.paper.score_t2_2}</td>
            <td>{assignment.paper.score_t2_3}</td>
            <td>{assignment.paper.score_t2_4}</td>
            <td>{assignment.paper.score_t2_5}</td>
          </tr>
        );
      });
    }
  },

  openModal: function(name, email, fn, event) {
    this.setState({
      modal_open: true,
      modal_name: name,
      modal_email: email,
      modal_onClick: fn,
      errors: {},
    });
    event.preventDefault();
  },

  closeModal: function(event) {
    this.setState({modal_open: false});
    event.preventDefault();
  },

  renderError: function(field) {
    if (this.state.errors[field]) {
      return (
        <StatusLabel status="error">{this.state.errors[field]}</StatusLabel>
      );
    }

    return null;
  },

  _handleDeleteDelegate: function(delegate) {
    const confirmed = window.confirm(
      `Are you sure you want to delete this delegate (${delegate.name})?`,
    );
    if (confirmed) {
      DelegateActions.deleteDelegate(delegate.id, this._handleDeleteError);
    }
  },

  _handleAddDelegate: function(data) {
    this.setState({loading: true});
    var user = CurrentUserStore.getCurrentUser();
    ServerAPI.createDelegate(
      this.state.modal_name,
      this.state.modal_email,
      user.school.id,
    ).then(this._handleAddDelegateSuccess, this._handleError);
    event.preventDefault();
  },

  _handleEditDelegate: function(delegate) {
    var user = CurrentUserStore.getCurrentUser();
    this.setState({loading: true});
    var delta = {name: this.state.modal_name, email: this.state.modal_email};
    DelegateActions.updateDelegate(delegate.id, delta, this._handleError);
    event.preventDefault();
  },

  _handleDelegatePasswordChange: function(delegate) {
    ServerAPI.resetDelegatePassword(delegate.id).then(
      this._handlePasswordChangeSuccess,
      this._handlePasswordChangeError,
    );
  },

  _handleAddDelegateSuccess: function(response) {
    DelegateActions.addDelegate(response);
    this.setState({
      loading: false,
      modal_open: false,
    });
  },

  _handlePasswordChangeSuccess: function(response) {
    this.setState({
      loading: false,
      modal_open: false,
    });
    window.alert(`Password successfully reset.`);
  },

  _handlePasswordChangeError: function(response) {
    window.alert(`The passowrd could not be reset.`);
  },

  _handleDeleteError: function(response) {
    window.alert(
      `There was an issue processing your request. Please refresh you page and try again.`,
    );
  },

  _handleError: function(response) {
    this.setState({
      errors: response,
      loading: false,
      modal_open: true,
    });
  },
});

module.exports = AdvisorPaperView;
