/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";
import { history } from "utils/history";
import type { Assignment, Committee, Note } from "utils/types";
import { NoteFeedBox } from "./notes/NoteFeedBox";

const { AssignmentStore } = require("stores/AssignmentStore");
const { Button } = require("components/core/Button");
const { CountryStore } = require("stores/CountryStore");
const { CurrentUserStore } = require("stores/CurrentUserStore");
const { InnerView } = require("components/InnerView");
const { TextTemplate } = require("components/core/TextTemplate");
const { User } = require("utils/User");
const { NoteConversation } = require("components/notes/NoteConversation");
const { NoteConversationHeader } = require("components/notes/NoteConversationHeader");
const {
  NoteConversationSelector,
} = require("components/notes/NoteConversationSelector");
const { NoteFeedFilter } = require("components/notes/NoteFeedFilter");
const { NoteSidebar } = require("components/notes/NoteSidebar");
const { NoteStore } = require("stores/NoteStore");

const { ServerAPI } = require("lib/ServerAPI");
// $FlowFixMe flow cannot currently understand markdown imports
const ChairFeedViewText = require("text/ChairFeedViewText.md");

const {
  _filterOnChairConversation,
  _getChairLastMessage,
  _isMessageFlagged,
} = require("utils/_noteFilters");

const PollingInterval = global.conference.polling_interval;

type ChairFeedViewState = {
  notes: Note[],
  committee_id: number,
  assignments: Array<Assignment>,
  countries: any,
  search_string: string,
  filter_sender: ?Assignment,
  filter_recipient: ?Assignment,
  filter_flagged: boolean,
};

class ChairFeedView extends React.Component<{}, ChairFeedViewState> {
  _conversationToken: any;
  _assignmentToken: any;
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
    const countries = CountryStore.getCountries();

    this.state = {
      notes: notes,
      committee_id: user_committee_id,
      assignments: assignments,
      countries: countries,
      search_string: "",
      filter_sender: null,
      filter_recipient: null,
      filter_flagged: false,
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

    this._countryToken = CountryStore.addListener(() => {
      this.setState({
        countries: CountryStore.getCountries(),
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
    this._countryToken && this._countryToken.remove();
    this._notePoller && clearInterval(this._notePoller);
  }

  render(): React$Element<any> {
    const country_map = {};
    const assignment_map = {};
    if (
      this.state.assignments.length &&
      Object.keys(this.state.countries).length
    ) {
      for (let assignment of this.state.assignments) {
        country_map[assignment.id] = this.state.countries[
          assignment.country
        ].name;
      }
    }

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
        <TextTemplate>{ChairFeedViewText}</TextTemplate>
        <NoteConversationHeader onRefreshNotes={this._onRefreshNotes}></NoteConversationHeader>
        <NoteFeedFilter
          assignments={assignment_map}
          onInputChange={this._onNoteSearch}
        />
        <NoteFeedBox
          notes={this._filterConversations(this.state.notes)}
          countries={country_map}
        />
      </InnerView>
    );
  }

  _onNoteSearch: (string, ?Assignment, ?Assignment, boolean) => void = (
    search_string,
    filter_sender,
    filter_recipient,
    filter_flagged
  ) => {
    this.setState({
      search_string,
      filter_sender,
      filter_recipient,
      filter_flagged,
    });
  };

  _filterFlaggedMessages: (Note[]) => Note[] = (notes) => {
    if (!this.state.filter_flagged) {
      return notes;
    }
    return notes.filter(_isMessageFlagged);
  };

  _filterConversations: (Note[]) => Note[] = (notes) => {
    return this._filterFlaggedMessages(
      this._filterConversationsByString(
        this._filterConversationsBySender(
          this._filterConversationsByRecipient(notes)
        )
      )
    );
  };

  _filterConversationsByString: (Note[]) => Note[] = (notes) => {
    if (this.state.search_string === "") {
      return notes;
    }
    return notes.filter(
      (note: Note) =>
        note.msg
          .toLowerCase()
          .search(this.state.search_string.toLowerCase()) !== -1
    );
  };

  _filterConversationsBySender: (Note[]) => Note[] = (notes) => {
    if (!this.state.filter_sender) {
      return notes;
    }
    return notes.filter(
      (note: Note) =>
        // $FlowFixMe this is fine, we return something if it doesn't exist
        note.sender === this.state.filter_sender.id
    );
  };

  _filterConversationsByRecipient: (Note[]) => Note[] = (notes) => {
    if (!this.state.filter_recipient) {
      return notes;
    }
    return notes.filter(
      (note: Note) =>
        // $FlowFixMe this is fine, we return something if it doesn't exist
        note.recipient === this.state.filter_recipient.id
    );
  };

  _onRefreshNotes: () => void = () => {
    this.setState({
      notes: NoteStore.getCommitteeNotes(this.state.committee_id),
    });
  };

}

export { ChairFeedView };
