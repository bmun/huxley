/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

//@flow

'use strict';

import React from "react";

const {Button} = require('components/core/Button');
const {TextTemplate} = require('components/core/TextTemplate');
const {NoteStore} = require('stores/NoteStore');


type NoteMessageBoxProps = {
    conversation: Array<any>,
    sender_id: number
}

class NoteMessageBox extends React.Component<NoteMessageBoxProps> {

  render(): any {
    return this.props.conversation.map(note => (note.sender === this.props.sender_id) ? this.renderSent(note.msg) : this.renderReceived(note.msg));
  }

  renderReceived: (string) => any = (msg) => {
    return <div className='received' style={{"textAlign": "left"}}>{msg}</div>;
  }

  renderSent: (string) => any = (msg) => {
    return <div className='sent' style={{"textAlign": "right"}}>{msg}</div>;
  }

}

export {NoteMessageBox};
