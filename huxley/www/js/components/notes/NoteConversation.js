/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

 //@flow

'use strict';

import React from "react";
import type { Note } from "utils/types";

const { InnerView } = require('components/InnerView');
const { NoteInputBox } = require('components/notes/NoteInputBox');
const { NoteMessageBox } = require('components/notes/NoteMessageBox');
const { NoteStore } = require('stores/NoteStore');

type NoteConversationProps = {
    sender_id: ?number,
    recipient_id: ?number,
    is_chair: number,
    conversation: Note[]
}

class NoteConversation extends React.Component<NoteConversationProps> {
    render(): any {
        return (
            <div>
                <NoteMessageBox conversation={this.props.conversation} sender_id={this.props.sender_id} />
                <NoteInputBox sender_id={this.props.sender_id} recipient_id={this.props.recipient_id} is_chair={this.props.is_chair} />
            </div>)
    }
};

export { NoteConversation };
