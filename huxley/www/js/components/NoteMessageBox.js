/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

//@flow

'use strict';

const Button = require('components/core/Button');
const TextTemplate = require('components/core/TextTemplate');


const cx = require('classnames');
const React = require('react');
type NoteMessageBoxProps = {
    conversation: Array<any>,
    user_assignment: number
}

class NoteMessageBox extends React.Component<NoteMessageBoxProps> {

  render(): any {
    return this.props.conversation.map(note => (note.sender === this.props.user_assignment) ? this.renderSent(note.msg) : this.renderReceived(note.msg));
  }

  renderReceived(msg: string): any {
    return <div className='received'>{msg}</div>;
  }

  renderSent(msg: string): any {
    return <div className='sent'>{msg}</div>;
  }

}

module.exports = NoteMessageBox;
