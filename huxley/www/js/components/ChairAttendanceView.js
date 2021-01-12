/**
* Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

"use strict";

import { React } from "react";
import history from "utils/history";

var Button = require("components/core/Button");
var AssignmentStore = require("stores/AssignmentStore");
var CountryStore = require("stores/CountryStore");
var CurrentUserStore = require("stores/CurrentUserStore");
var DelegateActions = require("actions/DelegateActions");
var DelegationAttendanceRow = require("components/DelegationAttendanceRow");
var DelegateStore = require("stores/DelegateStore");
var InnerView = require("components/InnerView");
var TextTemplate = require("components/core/TextTemplate");
var User = require("utils/User");

require("css/Table.less");
var ChairAttendanceViewText = require("text/ChairAttendanceViewText.md");

class ChairAttendanceView extends React.Component {
  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
    var countries = CountryStore.getCountries();
    var delegates = DelegateStore.getCommitteeDelegates(user.committee);
    var attendance = this._mapAttendance(delegates);
    if (assignments.length && Object.keys(countries).length) {
      assignments.sort((a1, a2) =>
        countries[a1.country].name < countries[a2.country].name ? -1 : 1
      );
    }

    return {
      loading: false,
      success: false,
      assignments: assignments,
      countries: countries,
      delegates: delegates,
      attendance: attendance,
    };
  }

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isChair(user)) {
      history.pushState(null, "/");
    }
  }

  componentDidMount() {
    var user = CurrentUserStore.getCurrentUser();
    var attendance = this.state.attendance;

    this._delegatesToken = DelegateStore.addListener(() => {
      var delegates = DelegateStore.getCommitteeDelegates(user.committee);
      var update = this._mapAttendance(delegates);
      this.setState({
        delegates: delegates,
        attendance: { ...attendance, ...update },
      });
    });

    this._assignmentsToken = AssignmentStore.addListener(() => {
      var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
      var countries = this.state.countries;
      if (Object.keys(countries).length) {
        assignments.sort((a1, a2) =>
          countries[a1.country].name < countries[a2.country].name ? -1 : 1
        );
      }
      this.setState({ assignments: assignments });
    });

    this._countriesToken = CountryStore.addListener(() => {
      var assignments = this.state.assignments;
      var countries = CountryStore.getCountries();
      if (assignments.length) {
        assignments.sort((a1, a2) =>
          countries[a1.country].name < countries[a2.country].name ? -1 : 1
        );
      }
      this.setState({
        assignments: assignments,
        countries: countries,
      });
    });
  }

  componentWillUnmount() {
    this._successTimout && clearTimeout(this._successTimeout);
    this._countriesToken && this._countriesToken.remove();
    this._delegatesToken && this._delegatesToken.remove();
    this._assignmentsToken && this._assignmentsToken.remove();
    this._successTimeout && clearTimeout(this._successTimeout);
  }

  render() {
    return (
      <InnerView>
        <TextTemplate>{ChairAttendanceViewText}</TextTemplate>
        <form>
          <div className="table-container">
            <table
              style={{ margin: "10px auto 0px auto", tableLayout: "fixed" }}
            >
              <thead>
                <tr>
                  <th>Assignment</th>
                  <th>Voting</th>
                  <th>Session One</th>
                  <th>Session Two</th>
                  <th>Session Three</th>
                  <th>Session Four</th>
                </tr>
              </thead>
            </table>
            <div style={{ overflowY: "auto", maxHeight: "50vh" }}>
              <table
                className="table highlight-cells"
                style={{ margin: "0px auto 20px auto", tableLayout: "fixed" }}
              >
                <tbody>{this.renderAttendanceRows()}</tbody>
              </table>
            </div>
          </div>
          <Button
            color="green"
            onClick={this._handleSaveAttendance}
            loading={this.state.loading}
            success={this.state.success}
          >
            Save Attendance
          </Button>
        </form>
      </InnerView>
    );
  }

  renderAttendanceRows() {
    var assignments = this.state.assignments;
    var attendance = this.state.attendance;
    var assignmentIDs = Object.keys(attendance);
    var countries = this.state.countries;
    assignments = assignments.filter(
      (a) => assignmentIDs.indexOf("" + a.id) > -1
    );
    return assignments.map((assignment) => (
      <DelegationAttendanceRow
        key={assignment.id}
        onChange={this._handleAttendanceChange}
        countryName={
          Object.keys(countries).length
            ? countries[assignment.country].name
            : "" + assignment.country
        }
        assignmentID={assignment.id}
        attendance={attendance[assignment.id]}
      />
    ));
  }

  _mapAttendance(delegates) {
    var attendance = {};
    for (var delegate of delegates) {
      attendance[delegate.assignment] = {
        voting: delegate.voting,
        session_one: delegate.session_one,
        session_two: delegate.session_two,
        session_three: delegate.session_three,
        session_four: delegate.session_four,
      };
    }
    return attendance;
  }

  _handleAttendanceChange(field, assignmentID, event) {
    var attendanceMap = this.state.attendance;
    var oldAttendance = attendanceMap[assignmentID];
    this.setState({
      attendance: {
        ...attendanceMap,
        [assignmentID]: { ...oldAttendance, [field]: !oldAttendance[field] },
      },
    });
  }

  _handleSaveAttendance(event) {
    this._successTimout && clearTimeout(this._successTimeout);
    this.setState({ loading: true });
    var committee = CurrentUserStore.getCurrentUser().committee;
    var attendanceMap = this.state.attendance;
    var delegates = this.state.delegates;
    var toSave = [];
    for (var delegate of delegates) {
      var attendance = attendanceMap[delegate.assignment];
      var shouldSave =
        delegate.voting !== attendance.voting ||
        delegate.session_one !== attendance.session_one ||
        delegate.session_two !== attendance.session_two ||
        delegate.session_three !== attendance.session_three ||
        delegate.session_four !== attendance.session_four;
      if (shouldSave) {
        toSave.push({
          ...delegate,
          voting: attendance.voting,
          session_one: attendance.session_one,
          session_two: attendance.session_two,
          session_three: attendance.session_three,
          session_four: attendance.session_four,
        });
      }
    }
    DelegateActions.updateCommitteeDelegates(
      committee,
      toSave,
      this._handleSuccess,
      this._handleError
    );
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

module.exports = ChairAttendanceView;
