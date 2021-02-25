/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";
import { history } from "utils/history";
import type { Assignment, Committee, Delegate, Note } from "utils/types";

const { AssignmentStore } = require("stores/AssignmentStore");
const { Button } = require("components/core/Button");
const { CommitteeActions } = require("actions/CommitteeActions");
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
  _filterOnChairConversation,
  _getChairLastMessage,
} = require("utils/_noteFilters");
const { PollingInterval } = require("constants/NoteConstants");
// $FlowFixMe flow cannot currently understand markdown imports
const ChairNoteViewText = require("text/ChairNoteViewText.md");
type ChairNoteViewState = {
  notes: Note[],
  recipient: ?Assignment,
  committee_id: number,
  assignments: Array<Assignment>,
  delegates: Array<Delegate>,
  countries: any,
  search_string: string,
  committees: { [number]: Committee },
};

class ChairNoteView extends React.Component<{}, ChairNoteViewState> {
  _conversationToken: any;
  _assignmentToken: any;
  _committeeToken: any;
  _delegateToken: any;
  _countryToken: any;
  _notePoller: IntervalID;

  constructor(props: {}) {
    super(props);
    const user = CurrentUserStore.getCurrentUser();
    const user_committee_id = user.committee;
    const notes = NoteStore.getCommitteeNotes(user_committee_id);
    const assignments = AssignmentStore.getCommitteeAssignments(
      user_committee_id
    );
    const delegates = DelegateStore.getCommitteeDelegates(user_committee_id);
    const committees = CommitteeStore.getCommittees();
    const countries = CountryStore.getCountries();

    this.state = {
      notes: notes,
      recipient: null,
      delegates: delegates,
      committee_id: user_committee_id,
      assignments: assignments,
      countries: countries,
      search_string: "",
      committees: committees,
    };
  }

  UNSAFE_componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isChair(user)) {
      history.redirect("/");
    }
  }

  componentDidMount() {
    this._conversationToken = NoteStore.addListener(() => {
      this.setState({
        notes: NoteStore.getCommitteeNotes(this.state.committee_id),
      });
    });

    this._assignmentToken = AssignmentStore.addListener(() => {
      this.setState({
        assignments: AssignmentStore.getCommitteeAssignments(
          this.state.committee_id
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
        delegates: DelegateStore.getCommitteeDelegates(this.state.committee_id),
      });
    });

    this._notePoller = setInterval(() => {
      this.setState({
        notes: NoteStore.getCommitteeNotes(this.state.committee_id),
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
          (last_message_map[country] = _getChairLastMessage(
            assignment_map[country].id,
            this.state.notes
          ))
      );
    }
    const recipient_name = this.state.recipient
      ? this.state.countries[this.state.recipient.country].name
      : "Chair";
    return (
      <InnerView>
        <TextTemplate>{ChairNoteViewText}</TextTemplate>
        {this._renderToggleButton()}
        <table width={"100%"}>
          <tbody>
            <tr>
              <td width={"25%"} style={{ verticalAlign: "top" }}>
                <NoteConversationSelector
                  assignments={assignment_map}
                  onChairConversationChange={() => {}}
                  onConversationChange={this._onConversationChange}
                  onInputChange={this._onCountrySearch}
                />
                <NoteSidebar
                  recipient_name={recipient_name}
                  assignments={this._filterAssignmentMap(assignment_map)}
                  last_messages={last_message_map}
                  display_chair={false}
                  onChairConversationChange={() => {}}
                  onConversationChange={this._onConversationChange}
                />
              </td>
              <td width={"75%"}>
                {this.state.recipient ? (
                  <NoteConversation
                    recipient_name={recipient_name}
                    sender_id={null}
                    recipient_id={
                      this.state.recipient ? this.state.recipient.id : null
                    }
                    is_chair={1}
                    conversation={_filterOnChairConversation(
                      this.state.recipient ? this.state.recipient.id : null,
                      this.state.notes
                    )}
                    onRefreshNotes={this._onRefreshNotes}
                  />
                ) : (
                  <div></div>
                )}
              </td>
            </tr>
          </tbody>
        </table>
      </InnerView>
    );
  }

  _onRefreshNotes: () => void = () => {
    this.setState({
      notes: NoteStore.getCommitteeNotes(this.state.committee_id),
    });
  };

  _renderToggleButton: () => any = () => {
    const activated = this.state.committees[this.state.committee_id]
      ? this.state.committees[this.state.committee_id].notes_activated
      : false;
    return (
      <div style={{ marginBottom: "5px" }}>
        <h3>
          Notes are currently{" "}
          {activated ? "on. " : "off. Delegates can only message the chair."}
        </h3>
        <Button
          color={activated ? "red" : "green"}
          size="medium"
          onClick={() =>
            CommitteeActions.updateCommittee(
              this.state.committee_id,
              { notes_activated: !activated },
              () => {}
            )
          }
        >
          Turn notes {activated ? "off" : "on"}?
        </Button>
      </div>
    );
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

export { ChairNoteView };
