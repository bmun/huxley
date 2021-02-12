/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";
import { history } from "utils/history";
import type { Assignment, Note } from "utils/types";

const { AssignmentStore } = require("stores/AssignmentStore");
const { Button } = require("components/core/Button");
const { CountryStore } = require("stores/CountryStore");
const { CurrentUserStore } = require("stores/CurrentUserStore");
const { InnerView } = require("components/InnerView");
const { TextTemplate } = require("components/core/TextTemplate");
const { User } = require("utils/User");
const { NoteConversation } = require("components/notes/NoteConversation");
const {
  NoteConversationSelector,
} = require("components/notes/NoteConversationSelector");
const { NoteSidebar } = require("components/notes/NoteSidebar");
const { NoteStore } = require("stores/NoteStore");

const { ServerAPI } = require("lib/ServerAPI");

const {
  _filterOnConversation,
  _getLastMessage,
} = require("utils/_noteFilters");
const { PollingInterval } = require("constants/NoteConstants");

type DelegateNoteViewState = {
  notes: {[string]: Note},
  recipient: any,
  sender: any,
  assignments: Array<Assignment>,
  countries: any,
  search_string: string,
};

class DelegateNoteView extends React.Component<{}, DelegateNoteViewState> {
  _conversationToken: any;
  _assignmentToken: any;
  _countryToken: any;
  _notePoller: IntervalID;

  constructor(props: {}) {
    super(props);
    const user = CurrentUserStore.getCurrentUser();
    const user_assignment = user.delegate.assignment;
    const notes = NoteStore.getConversationNotes(
      user_assignment.id,
      null,
      true
    );
    const assignments = AssignmentStore.getCommitteeAssignments(
      user_assignment.committee.id
    );
    const countries = CountryStore.getCountries();

    this.state = {
      notes: notes,
      recipient: null,
      sender: user_assignment,
      assignments: assignments,
      countries: countries,
      search_string: "",
    };
  }

  UNSAFE_componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isDelegate(user)) {
      history.redirect("/");
    }
  }

  componentDidMount() {
    this._conversationToken = NoteStore.addListener(() => {
      this.setState({
        notes: NoteStore.getConversationNotes(
          this.state.sender.id,
          this.state.recipient ? this.state.recipient.id : null,
          this.state.recipient ? 0 : 2
        ),
      });
    });

    this._assignmentToken = AssignmentStore.addListener(() => {
      this.setState({
        assignments: AssignmentStore.getCommitteeAssignments(
          this.state.sender.committee.id
        ),
      });
    });

    this._countryToken = CountryStore.addListener(() => {
      this.setState({
        countries: CountryStore.getCountries(),
      });
    });

    this._notePoller = setInterval(() => {
      this.setState({
        notes: NoteStore.getConversationNotes(
          this.state.sender.id,
          this.state.recipient ? this.state.recipient.id : null,
          this.state.recipient ? 0 : 2
        ),
      });
    }, PollingInterval);
  }

  componentWillUnmount() {
    this._conversationToken && this._conversationToken.remove();
    this._assignmentToken && this._assignmentToken.remove();
    this._countryToken && this._countryToken.remove();
    clearInterval(this._notePoller);
  }

  render(): React$Element<any> {
    const assignment_map = {};
    const last_message_map = {};
    if (
      this.state.assignments.length &&
      Object.keys(this.state.countries).length
    ) {
      for (let assignment of this.state.assignments) {
        assignment_map[
          this.state.countries[assignment.country].name
        ] = assignment;
      }
    }
    if (assignment_map && this.state.notes) {
      Object.keys(assignment_map).map(
        (country) =>
          (last_message_map[country] = _getLastMessage(
            this.state.sender.id,
            assignment_map[country].id,
            false,
            this.state.notes
          ))
      );
      last_message_map["Chair"] = _getLastMessage(
        this.state.sender.id,
        null,
        true,
        this.state.notes
      );
    }
    const recipient_name = this.state.recipient
      ? this.state.countries[this.state.recipient.country].name
      : "Chair";
    return (
      <InnerView>
        <table width={"100%"}>
          <tbody>
            <tr>
              <td width={"25%"} style={{ verticalAlign: "top" }}>
                <NoteConversationSelector
                  assignments={assignment_map}
                  onChairConversationChange={this._onChairConversationChange}
                  onConversationChange={this._onConversationChange}
                  onInputChange={this._onCountrySearch}
                />
                <NoteSidebar
                  recipient_name={recipient_name}
                  assignments={this._filterAssignmentMap(assignment_map)}
                  last_messages={last_message_map}
                  onChairConversationChange={this._onChairConversationChange}
                  onConversationChange={this._onConversationChange}
                />
              </td>
              <td width={"75%"}>
                <NoteConversation
                  recipient_name={recipient_name}
                  sender_id={this.state.sender.id}
                  recipient_id={
                    this.state.recipient ? this.state.recipient.id : null
                  }
                  is_chair={this.state.recipient ? 0 : 2}
                  conversation={_filterOnConversation(
                    this.state.sender.id,
                    this.state.recipient ? this.state.recipient.id : null,
                    this.state.recipient == null,
                    this.state.notes
                  )}
                />
              </td>
            </tr>
          </tbody>
        </table>
      </InnerView>
    );
  }

  _onChairConversationChange: () => void = () => {
    this.setState({
      notes: NoteStore.getConversationNotes(this.state.sender.id, null, true),
      recipient: null,
    });
  };

  _onConversationChange: (Assignment) => void = (recipient) => {
    this.setState({
      notes: NoteStore.getConversationNotes(
        this.state.sender.id,
        recipient.id,
        false
      ),
      recipient: recipient,
    });
  };

  _onCountrySearch: (string) => void = (search_string) => {
    this.setState({
      search_string: search_string,
    });
  };

  _filterAssignmentMap: ({ [string]: Assignment }) => { [string]: Assignment } = (
    assignment_map
  ) => {
    if (this.state.search_string === "") {
      return assignment_map;
    }
    const filtered_assignment_map = {};
    Object.keys(assignment_map).map((country) => {
      if (
        country.toLowerCase().search(this.state.search_string.toLowerCase()) !==
        -1
      ) {
        filtered_assignment_map[country] = assignment_map[country];
      }
    });
    return filtered_assignment_map;
  };
}

export { DelegateNoteView };
