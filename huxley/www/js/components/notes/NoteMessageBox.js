/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

//@flow

"use strict";

import React from "react";

const { Button } = require("components/core/Button");
const { TextTemplate } = require("components/core/TextTemplate");
const { NoteStore } = require("stores/NoteStore");

// $FlowFixMe
require("css/notes/NoteMessageBox.less");

type NoteMessageBoxProps = {
  conversation: Array<any>,
  sender_id: ?number,
};

class NoteMessageBox extends React.Component<NoteMessageBoxProps> {
  messageBox: ?HTMLDivElement;
  render(): any {
    return (
      <div class="messageBox" ref = {(el) => { this.messageBox = el; }}>
        <div>
          {this.props.conversation.map((note) =>
            note.sender === this.props.sender_id
              ? this.renderSent(note.msg)
              : this.renderReceived(note.msg)
          )}
        </div>
      </div>
    );
  }

  componentDidMount() {
    if (this.messageBox) {
      this.messageBox.scrollTop = this.messageBox.scrollHeight;
    }
  }
  
  componentDidUpdate() {
    if (this.messageBox) {
      this.messageBox.scrollTop = this.messageBox.scrollHeight;
    }
  }
  

  renderReceived: (string) => any = (msg) => {
    return <div className="message received">{msg}</div>;
  };

  renderSent: (string) => any = (msg) => {
    return <div className="message sent">{msg}</div>;
  };
}

export { NoteMessageBox };
