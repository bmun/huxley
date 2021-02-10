/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";
import { history } from "utils/history";

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
const { NoteStore } = require("stores/NoteStore");

const { ServerAPI } = require("lib/ServerAPI");

type DelegateNoteViewState = {
  conversation: Array<any>,
  recipient: any,
  sender: any,
  assignments: Array<any>,
  countries: any,
};

class DelegateNoteView extends React.Component<{}, DelegateNoteViewState> {
  _conversationToken: any;
  _assignmentToken: any;
  _countryToken: any;

  constructor(props: {}) {
    super(props);
    const user = CurrentUserStore.getCurrentUser();
    const user_assignment = user.delegate.assignment;
    const conversation = NoteStore.getConversationNotes(
      user_assignment.id,
      null,
      true
    );
    const assignments = AssignmentStore.getCommitteeAssignments(
      user_assignment.committee.id
    );
    const countries = CountryStore.getCountries();

    this.state = {
      conversation: conversation,
      recipient: null,
      sender: user_assignment,
      assignments: assignments,
      countries: countries,
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
        conversation: NoteStore.getConversationNotes(
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
  }

  componentWillUnmount() {
    this._conversationToken && this._conversationToken.remove();
    this._assignmentToken && this._assignmentToken.remove();
    this._countryToken && this._countryToken.remove();
  }

  render(): any {
    const assignment_map = {};
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
                />
              </td>
              <td width={"75%"}>
                <NoteConversation
                  sender_id={this.state.sender.id}
                  recipient_id={
                    this.state.recipient ? this.state.recipient.id : null
                  }
                  is_chair={this.state.recipient ? 0 : 2}
                  conversation={this.state.conversation}
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
      conversation: NoteStore.getConversationNotes(
        this.state.sender.id,
        null,
        true
      ),
      recipient: null,
    });
  };

  _onConversationChange: (any) => void = (recipient) => {
    this.setState({
      conversation: NoteStore.getConversationNotes(
        this.state.sender.id,
        recipient.id,
        false
      ),
      recipient: recipient,
    });
  };
}

export { DelegateNoteView };
