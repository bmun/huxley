/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

//@flow

"use strict";

import React from "react";

const { Button } = require("components/core/Button");
const { TextTemplate } = require("components/core/TextTemplate");
const { NoteActions } = require("actions/NoteActions");
const { NoteStore } = require("stores/NoteStore");
const { ServerAPI } = require("lib/ServerAPI");

// $FlowFixMe
require("css/notes/NoteInputBox.less");
type NoteInputBoxProps = {
  sender_id: ?number,
  recipient_id: ?number,
  is_chair: number,
};

type NoteInputBoxState = {
  msg: string,
};

class NoteInputBox extends React.Component<
  NoteInputBoxProps,
  NoteInputBoxState
> {
  static defaultProps: NoteInputBoxProps = {
    sender_id: null,
    recipient_id: null,
    is_chair: 0,
  };
  constructor(props: NoteInputBoxProps) {
    super(props);

    this.state = {
      msg: "",
    };
  }

  render(): React$Element<any> {
    return (
      <div className="inputBox">
        <form onSubmit={this._handleSubmit}>
          <input
            className="noteInput"
            type="text"
            value={this.state.msg}
            onChange={this._handleChange}
            maxLength="1000"
          />
          <input type="submit" style={{ display: "none" }} />
        </form>
        <Button className="sendButton" size="small" onClick={this._handleSubmit} color="blue">
          Send
        </Button>
      </div>
    );
  }

  _handleChange: (SyntheticEvent<HTMLInputElement>) => void = (event) => {
    if (event.target instanceof HTMLInputElement)
    this.setState({ msg: event.target.value });
  };

  _handleSubmit: (SyntheticEvent<HTMLInputElement>) => void = (event) => {
    if (this.state.msg.trim() !== "") {
      ServerAPI.createNote(
        this.props.is_chair,
        this.props.sender_id,
        this.props.recipient_id,
        this.state.msg
      ).then(this._handleNoteInputSuccess, this._handleNoteInputError);
    }
    event.preventDefault();
  };

  _handleNoteInputSuccess: (any) => void = (response) => {
    NoteActions.addNote(response);
    this.setState({ msg: "" });
  };

  _handleNoteInputError: (any) => void = (response) => {
    window.alert(`Message was unable to be sent: ${response['reason']}`);
  };
}

export { NoteInputBox };
