/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

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

class NoteConversation extends React.Component {
    static defaultProps : NoteInputBoxProps = {
        sender_id: null,
        recipient_id: null,
        is_chair: 0
    }

    render() {
        return (
            <div>
                <NoteMessageBox conversation={this.props.conversation} sender_id={this.props.sender_id} />
                <NoteInputBox sender_id={this.props.sender_id} is_chair={this.props.is_chair} />
            </div>)
    }
};

export { NoteConversation };
