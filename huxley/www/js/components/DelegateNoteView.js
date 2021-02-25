/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";
import { history } from "utils/history";
import type {
  Assignment,
  AssignmentNested,
  Committee,
  Delegate,
  Note,
} from "utils/types";

const { AssignmentStore } = require("stores/AssignmentStore");
const { Button } = require("components/core/Button");
const { CommitteeStore } = require("stores/CommitteeStore");
const { CountryStore } = require("stores/CountryStore");
const { CurrentUserStore } = require("stores/CurrentUserStore");
const { DelegateStore } = require("stores/DelegateStore");
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
// $FlowFixMe flow cannot currently understand markdown imports
const DelegateNoteViewText = require("text/DelegateNoteViewText.md");
// $FlowFixMe flow cannot currently understand markdown imports
const DelegateNoteDisabledViewText = require("text/DelegateNoteDisabledViewText.md");

type DelegateNoteViewState = {
  notes: Note[],
  recipient: ?Assignment,
  sender: AssignmentNested,
  assignments: Array<Assignment>,
  delegates: Array<Delegate>,
  countries: any,
  search_string: string,
  committees: { [number]: Committee },
};

class DelegateNoteView extends React.Component<{}, DelegateNoteViewState> {
  _conversationToken: any;
  _assignmentToken: any;
  _committeeToken: any;
  _delegateToken: any;
  _countryToken: any;
  _notePoller: IntervalID;

  constructor(props: {}) {
    super(props);
    const user = CurrentUserStore.getCurrentUser();
    const user_assignment = user.delegate.assignment;
    const notes = NoteStore.getConversationNotes(user_assignment.id);
    const assignments = AssignmentStore.getCommitteeAssignments(
      user_assignment.committee.id
    );
    const delegates = DelegateStore.getCommitteeDelegates(
      user_assignment.committee.id
    );
    const countries = CountryStore.getCountries();
    const committees = CommitteeStore.getCommittees();

    this.state = {
      notes: notes,
      recipient: null,
      delegates: delegates,
      sender: user_assignment,
      assignments: assignments,
      countries: countries,
      search_string: "",
      committees: committees,
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
        notes: NoteStore.getConversationNotes(this.state.sender.id),
      });
    });

    this._assignmentToken = AssignmentStore.addListener(() => {
      this.setState({
        assignments: AssignmentStore.getCommitteeAssignments(
          this.state.sender.committee.id
        ),
      });
    });

    this._committeeToken = CommitteeStore.addListener(() => {
      this.setState({
        committees: CommitteeStore.getCommittees(),
      });
    });

    this._countryToken = CountryStore.addListener(() => {
      this.setState({
        countries: CountryStore.getCountries(),
      });
    });

    this._delegateToken = DelegateStore.addListener(() => {
      this.setState({
        delegates: DelegateStore.getCommitteeDelegates(
          this.state.sender.committee.id
        ),
      });
    });

    this._notePoller = setInterval(() => {
      this.setState({
        notes: NoteStore.getConversationNotes(this.state.sender.id),
      });
    }, PollingInterval);
  }

  componentWillUnmount() {
    this._conversationToken && this._conversationToken.remove();
    this._assignmentToken && this._assignmentToken.remove();
    this._committeeToken && this._committeeToken.remove();
    this._countryToken && this._countryToken.remove();
    this._delegateToken && this._delegateToken.remove();
    clearInterval(this._notePoller);
  }

  render(): React$Element<any> {
    const activated = this.state.committees[this.state.sender.committee.id]
      ? this.state.committees[this.state.sender.committee.id].notes_activated
      : false;

    if (!global.conference.notes_enabled) {
      return (
        <InnerView>
          <TextTemplate>{DelegateNoteViewText}</TextTemplate>
          <TextTemplate>{DelegateNoteDisabledViewText}</TextTemplate>
        </InnerView>
      );
    }

    const assignmentIDs = this.state.delegates.map(
      (delegate) => delegate.assignment
    );

    const assignments = this.state.assignments.filter((assignment) =>
      assignmentIDs.includes(assignment.id)
    );

    const assignment_map = {};
    const last_message_map = {};
    if (assignments.length && Object.keys(this.state.countries).length) {
      for (let assignment of assignments) {
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
        <TextTemplate>{DelegateNoteViewText}</TextTemplate>
        {/* {!activated ? <div><h3>Notes are currently disabled. You may still message the chair.</h3></div> : <div></div>} */}
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
                  display_chair={true}
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
                  onRefreshNotes={this._onRefreshNotes}
                />
              </td>
            </tr>
          </tbody>
        </table>
      </InnerView>
    );
  }

  _onRefreshNotes: () => void = () => {
    this.setState({
      notes: NoteStore.getConversationNotes(this.state.sender.id),
    });
  };

  _onChairConversationChange: () => void = () => {
    this.setState({
      recipient: null,
    });
  };

  _onConversationChange: (Assignment) => void = (recipient) => {
    this.setState({
      recipient: recipient,
    });
  };

  _onCountrySearch: (string) => void = (search_string) => {
    this.setState({
      search_string: search_string,
    });
  };

  _filterAssignmentMap: ({ [string]: Assignment }) => {
    [string]: Assignment,
  } = (assignment_map) => {
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
