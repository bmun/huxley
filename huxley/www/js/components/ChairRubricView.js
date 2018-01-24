/**
* Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

const React = require('react');
const ReactRouter = require('react-router');

const Button = require('components/core/Button');
const CommitteeStore = require('stores/CommitteeStore');
const CurrentUserStore = require('stores/CurrentUserStore');
const InnerView = require('components/InnerView');
const NumberInput = require('components/NumberInput');
const RubricActions = require('actions/RubricActions');
const RubricStore = require('stores/RubricStore');
const TextInput = require('components/core/TextInput');
const TextTemplate = require('components/core/TextTemplate');
const User = require('utils/User');

require('css/Table.less');
const ChairRubricText = require('text/ChairRubricViewText.md');

const ChairRubricView = React.createClass({
  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    var committees = CommitteeStore.getCommittees();
    var rubric = null;
    if (Object.keys(committees).length) {
      var committee = committees[user.committee];
      rubric = RubricStore.getRubric(committee.rubric.id);
    }
    return {
      loading: false,
      success: false,
      committees: committees,
      rubric: rubric,
    };
  },

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isChair(user)) {
      this.history.pushState(null, '/');
    }
  },

  componentDidMount() {
    this._committeesToken = CommitteeStore.addListener(() => {
      var user = CurrentUserStore.getCurrentUser();
      var committees = CommitteeStore.getCommittees();
      var committee = committees[user.committee];
      this.setState({committees: committees});
      RubricStore.getRubric(committee.rubric.id);
    });

    this._rubricToken = RubricStore.addListener(() => {
      var committees = this.state.committees;
      var user = CurrentUserStore.getCurrentUser();
      if (user.committee in committees) {
        var committee = committees[user.committee];
        this.setState({rubric: RubricStore.getRubric(committee.rubric.id)});
      }
    });
  },

  componentWillUnmount() {
    this._rubricToken && this._rubricToken.remove();
    this._successTimeout && clearTimeout(this._successTimeout);
  },

  render() {
    var rubric = this.state.rubric;
    if (rubric == null) {
      return <InnerView>
                <div>Waiting for server...</div>
             </InnerView>
    }

    return <InnerView>
              <TextTemplate>
                {ChairRubricText}
              </TextTemplate>
              <form>
                <table>
                  <thead>
                    <tr>
                      <th>Category</th>
                      <th>Maximum Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>
                        <TextInput
                          defaultValue={rubric.grade_category_1}
                          onChange={this._handleChange.bind(this, "grade_category_1")}
                        />
                      </td>
                      <td>
                        <NumberInput
                          defaultValue={""+rubric.grade_value_1}
                          onChange={this._handleValueChange.bind(this, "grade_value_1")}
                        />
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <TextInput
                          defaultValue={rubric.grade_category_2}
                          onChange={this._handleChange.bind(this, "grade_category_2")}
                        />
                      </td>
                      <td>
                        <NumberInput
                          defaultValue={""+rubric.grade_value_2}
                          onChange={this._handleValueChange.bind(this, "grade_value_2")}
                        />
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <TextInput
                          defaultValue={rubric.grade_category_3}
                          onChange={this._handleChange.bind(this, "grade_category_3")}
                        />
                      </td>
                      <td>
                        <NumberInput
                          defaultValue={""+rubric.grade_value_3}
                          onChange={this._handleValueChange.bind(this, "grade_value_3")}
                        />
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <TextInput
                          defaultValue={rubric.grade_category_4}
                          onChange={this._handleChange.bind(this, "grade_category_4")}
                        />
                      </td>
                      <td>
                        <NumberInput
                          defaultValue={""+rubric.grade_value_4}
                          onChange={this._handleValueChange.bind(this, "grade_value_4")}
                        />
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <TextInput
                          defaultValue={rubric.grade_category_5}
                          onChange={this._handleChange.bind(this, "grade_category_5")}
                        />
                      </td>
                      <td>
                        <NumberInput
                          defaultValue={""+rubric.grade_value_5}
                          onChange={this._handleValueChange.bind(this, "grade_value_5")}
                        />
                      </td>
                    </tr>
                  </tbody>
                </table>
                <Button
                  onClick={this._handleSaveRubric}>
                  Save
                </Button>
              </form>
            </InnerView>
  },

  _handleChange (field, event) {
    var rubric = this.state.rubric;
    this.setState({
      rubric: {
        ...rubric,
        [field]: event,
      },
    });
  },

  _handleValueChange (field, event) {
    var rubric = this.state.rubric;
    this.setState({
      rubric: {
        ...rubric,
        [field]: Number(event),
      },
    });
  },

  _handleSaveRubric(event) {
    this.setState({loading: true});
    this._successTimout && clearTimeout(this._successTimeout);
    var rubric = {...this.state.rubric};
    RubricActions.updateRubric(
      rubric,
      this._handleSuccess,
      this._handleError,
    );
    event.preventDefault();
  },

  _handleSuccess: function(response) {
    this.setState({
      loading: false,
      success: true,
    });

    this._successTimeout = setTimeout(
      () => this.setState({success: false}),
      2000,
    );
  },

  _handleError: function(response) {
    this.setState({loading: false});
    window.alert(
      'Something went wrong. Please refresh your page and try again.',
    );
  },
});

module.exports = ChairRubricView;
