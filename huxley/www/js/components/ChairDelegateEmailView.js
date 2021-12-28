/**
* Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

"use strict";

import React from "react";
import { history } from "utils/history";
import { Table } from "./core/Table";

var { AssignmentStore } = require("stores/AssignmentStore");
var { Button } = require("components/core/Button");
var { CountryStore } = require("stores/CountryStore");
var { CurrentUserStore } = require("stores/CurrentUserStore");
var { DelegateStore } = require("stores/DelegateStore");
var { InnerView } = require("components/InnerView");
var { TextTemplate } = require("components/core/TextTemplate");
var { User } = require("utils/User");

require("css/Table.less");
var ChairDelegateEmailViewText = require("text/ChairDelegateEmailViewText.md");

class ChairDelegateEmailView extends React.Component {
  constructor(props) {
    super(props);
    var user = CurrentUserStore.getCurrentUser();
    var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
    var countries = CountryStore.getCountries();
    var delegates = DelegateStore.getCommitteeDelegates(user.committee);

    if (assignments.length && Object.keys(countries).length) {
      assignments.sort((a1, a2) =>
        countries[a1.country].name < countries[a2.country].name ? -1 : 1
      );
    }

    this.state = {
      assignments: assignments,
      countries: countries,
      delegates: delegates,
    };
  }

  UNSAFE_componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isChair(user)) {
      history.redirect("/");
    }
  }

  componentDidMount() {
    var user = CurrentUserStore.getCurrentUser();

    this._delegatesToken = DelegateStore.addListener(() => {
      var delegates = DelegateStore.getCommitteeDelegates(user.committee);
      this.setState({ delegates: delegates });
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
    this._countriesToken && this._countriesToken.remove();
    this._delegatesToken && this._delegatesToken.remove();
    this._assignmentsToken && this._assignmentsToken.remove();
  }

  render() {
    return (
      <InnerView>
        <TextTemplate style={{width: "50%"}}>{ChairDelegateEmailViewText}</TextTemplate>
        <form>
          <Table
            emptyMessage="You don't have any delegates in your committee."
            isEmpty={!this.state.delegates.length}
          >
            <thead>
              <tr>
                <th>Assignment</th>
                <th>Email
                  <Button
                    color="blue"
                    size="small"
                    style={{float: "right"}}
                    onClick={this._copyEmailsToClipboard}
                  >
                    Copy emails to clipboard
                  </Button>
                </th>
              </tr>
            </thead>
            <tbody>
              {Object.keys(this.state.countries).length > 0 ? (
                this.renderEmailRows()
              ) : (
                <tr />
              )}
            </tbody>
          </Table>
        </form>
      </InnerView>
    );
  }

  renderEmailRows = () => {
    var assignments = this.state.assignments;
    var delegates = this.state.delegates;
    var countries = this.state.countries;
    return delegates.map((delegate) => {
      return (
        <tr key={delegate.id}>
          <td>
            {
              countries[
                assignments.find((a) => a.id == delegate.assignment).country
              ].name
            }
          </td>
          <td>{delegate.email}</td>
        </tr>
      );
    });
  };

  _copyEmailsToClipboard = (event) => {
    var str = '';
    for (var del of this.state.delegates) {
      str += del.email;
      str += ", ";
    }
    navigator.clipboard.writeText(str);
    event.preventDefault();
  }
}

export { ChairDelegateEmailView };
