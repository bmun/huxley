/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

"use strict";

import React from "react";
import PropTypes from "prop-types";
import history from "utils/history";

const Button = require("components/core/Button");
const CommitteeStore = require("stores/CommitteeStore");
const CurrentUserStore = require("stores/CurrentUserStore");
const InnerView = require("components/InnerView");
const NumberInput = require("components/NumberInput");
const RubricActions = require("actions/RubricActions");
const RubricStore = require("stores/RubricStore");
const TextInput = require("components/core/TextInput");
const TextTemplate = require("components/core/TextTemplate");
const User = require("utils/User");

require("css/Table.less");
const ChairRubricText = require("text/ChairRubricViewText.md");

class ChairRubricView extends React.Component {
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
  }

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isChair(user)) {
      history.pushState(null, "/");
    }
  }

  componentDidMount() {
    this._committeesToken = CommitteeStore.addListener(() => {
      var user = CurrentUserStore.getCurrentUser();
      var committees = CommitteeStore.getCommittees();
      var committee = committees[user.committee];
      this.setState({ committees: committees });
      RubricStore.getRubric(committee.rubric.id);
    });

    this._rubricToken = RubricStore.addListener(() => {
      var committees = this.state.committees;
      var user = CurrentUserStore.getCurrentUser();
      if (user.committee in committees) {
        var committee = committees[user.committee];
        this.setState({ rubric: RubricStore.getRubric(committee.rubric.id) });
      }
    });
  }

  componentWillUnmount() {
    this._rubricToken && this._rubricToken.remove();
    this._successTimeout && clearTimeout(this._successTimeout);
  }

  render() {
    var rubric = this.state.rubric;
    if (rubric == null) {
      return (
        <InnerView>
          <div>Waiting for server...</div>
        </InnerView>
      );
    }

    var secondRubric = rubric.use_topic_2 ? (
      this._renderTopicTwo(rubric)
    ) : (
      <div />
    );

    var secondTopic = rubric.use_topic_2 ? (
      <table>
        <tbody>
          <tr>
            <td>
              <div>Topic Two: &emsp; &emsp; &emsp; </div>
            </td>
            <td>
              <TextInput
                defaultValue={rubric.topic_two}
                onChange={this._handleChange.bind(this, "topic_two")}
              />
            </td>
          </tr>
          <tr>
            <td>
              <br />
            </td>
          </tr>
        </tbody>
      </table>
    ) : (
      <div />
    );

    return (
      <InnerView>
        <TextTemplate>{ChairRubricText}</TextTemplate>
        <form>
          <table>
            <tbody>
              <tr>
                <td>Use second topic: &emsp; </td>
                <td>
                  <input
                    className="choice"
                    type="checkbox"
                    checked={rubric.use_topic_2}
                    onChange={this._handleChange.bind(this, "use_topic_2")}
                  />
                </td>
              </tr>
              <tr>
                <td>
                  <br />
                </td>
              </tr>
              <tr>
                <td>
                  <div>Topic One: </div>
                </td>
                <td>
                  <TextInput
                    defaultValue={rubric.topic_one}
                    onChange={this._handleChange.bind(this, "topic_one")}
                  />
                </td>
              </tr>
              <tr>
                <td>
                  <br />
                </td>
              </tr>
            </tbody>
          </table>
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
                    defaultValue={"" + rubric.grade_value_1}
                    onChange={this._handleValueChange.bind(
                      this,
                      "grade_value_1"
                    )}
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
                    defaultValue={"" + rubric.grade_value_2}
                    onChange={this._handleValueChange.bind(
                      this,
                      "grade_value_2"
                    )}
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
                    defaultValue={"" + rubric.grade_value_3}
                    onChange={this._handleValueChange.bind(
                      this,
                      "grade_value_3"
                    )}
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
                    defaultValue={"" + rubric.grade_value_4}
                    onChange={this._handleValueChange.bind(
                      this,
                      "grade_value_4"
                    )}
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
                    defaultValue={"" + rubric.grade_value_5}
                    onChange={this._handleValueChange.bind(
                      this,
                      "grade_value_5"
                    )}
                  />
                </td>
              </tr>
              <tr>
                <td>
                  <br />
                </td>
              </tr>
            </tbody>
          </table>
          {secondTopic}
          {secondRubric}
          <Button
            onClick={this._handleSaveRubric}
            loading={this.state.loading}
            success={this.state.success}
          >
            Save
          </Button>
        </form>
      </InnerView>
    );
  }

  _renderTopicTwo(rubric) {
    return (
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
                defaultValue={rubric.grade_t2_category_1}
                onChange={this._handleChange.bind(this, "grade_t2_category_1")}
              />
            </td>
            <td>
              <NumberInput
                defaultValue={"" + rubric.grade_t2_value_1}
                onChange={this._handleValueChange.bind(
                  this,
                  "grade_t2_value_1"
                )}
              />
            </td>
          </tr>
          <tr>
            <td>
              <TextInput
                defaultValue={rubric.grade_t2_category_2}
                onChange={this._handleChange.bind(this, "grade_t2_category_2")}
              />
            </td>
            <td>
              <NumberInput
                defaultValue={"" + rubric.grade_t2_value_2}
                onChange={this._handleValueChange.bind(
                  this,
                  "grade_t2_value_2"
                )}
              />
            </td>
          </tr>
          <tr>
            <td>
              <TextInput
                defaultValue={rubric.grade_t2_category_3}
                onChange={this._handleChange.bind(this, "grade_t2_category_3")}
              />
            </td>
            <td>
              <NumberInput
                defaultValue={"" + rubric.grade_t2_value_3}
                onChange={this._handleValueChange.bind(
                  this,
                  "grade_t2_value_3"
                )}
              />
            </td>
          </tr>
          <tr>
            <td>
              <TextInput
                defaultValue={rubric.grade_t2_category_4}
                onChange={this._handleChange.bind(this, "grade_t2_category_4")}
              />
            </td>
            <td>
              <NumberInput
                defaultValue={"" + rubric.grade_t2_value_4}
                onChange={this._handleValueChange.bind(
                  this,
                  "grade_t2_value_4"
                )}
              />
            </td>
          </tr>
          <tr>
            <td>
              <TextInput
                defaultValue={rubric.grade_t2_category_5}
                onChange={this._handleChange.bind(this, "grade_t2_category_5")}
              />
            </td>
            <td>
              <NumberInput
                defaultValue={"" + rubric.grade_t2_value_5}
                onChange={this._handleValueChange.bind(
                  this,
                  "grade_t2_value_5"
                )}
              />
            </td>
          </tr>
        </tbody>
      </table>
    );
  }

  _handleChange(field, event) {
    var rubric = this.state.rubric;
    if (field == "use_topic_2") {
      event = !rubric.use_topic_2;
    }
    this.setState({
      rubric: {
        ...rubric,
        [field]: event,
      },
    });
  }

  _handleValueChange(field, event) {
    var rubric = this.state.rubric;
    this.setState({
      rubric: {
        ...rubric,
        [field]: Number(event),
      },
    });
  }

  _handleSaveRubric(event) {
    this.setState({ loading: true });
    this._successTimout && clearTimeout(this._successTimeout);
    var rubric = { ...this.state.rubric };
    RubricActions.updateRubric(rubric, this._handleSuccess, this._handleError);
    event.preventDefault();
  }

  _handleSuccess(response) {
    this.setState({
      loading: false,
      success: true,
    });

    this._successTimeout = setTimeout(
      () => this.setState({ success: false }),
      2000
    );
  }

  _handleError(response) {
    this.setState({ loading: false });
    window.alert(
      "Something went wrong. Please refresh your page and try again."
    );
  }
}


