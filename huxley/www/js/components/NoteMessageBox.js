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
    user_assignment: number
}

class NoteMessageBox extends React.Component<NoteMessageBoxProps> {

  render(): any {
    console.log(this.props.conversation);
    return this.props.conversation.map(note => (note.sender === this.props.user_assignment) ? this.renderSent(note.msg) : this.renderReceived(note.msg));
  }

  renderReceived = (msg: string) : any => {
    return <div className='received'>{msg}</div>;
  }

  renderSent = (msg: string): any => {
    return <div className='sent'>{msg}</div>;
  }

}

export {NoteMessageBox};
