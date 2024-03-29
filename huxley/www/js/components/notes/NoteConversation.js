/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";
import type { Note } from "utils/types";

const {
  NoteConversationHeader,
} = require("components/notes/NoteConversationHeader");
const { NoteInputBox } = require("components/notes/NoteInputBox");
const { NoteMessageBox } = require("components/notes/NoteMessageBox");

type NoteConversationProps = {
  recipient_name: ?string,
  sender_id: ?number,
  recipient_id: ?number,
  is_chair: number,
  conversation: Note[],
  onRefreshNotes: () => void,
};

class NoteConversation extends React.Component<NoteConversationProps> {
  render(): React$Element<any> {
    return (
      <div>
        <NoteConversationHeader
          recipient_name={this.props.recipient_name}
          onRefreshNotes={this.props.onRefreshNotes}
        />
        <NoteMessageBox
          conversation={this.props.conversation}
          sender_id={this.props.sender_id}
        />
        <NoteInputBox
          sender_id={this.props.sender_id}
          recipient_id={this.props.recipient_id}
          is_chair={this.props.is_chair}
        />
      </div>
    );
  }
}

export { NoteConversation };
