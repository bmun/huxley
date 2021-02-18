/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

//@flow

"use strict";

import React from "react";
import type { Note } from "utils/types";

const { Button } = require("components/core/Button");
const { TextTemplate } = require("components/core/TextTemplate");
const { NoteStore } = require("stores/NoteStore");

// $FlowFixMe
require("css/notes/NoteFeedBubble.less");

type NoteFeedBubbleProps = {
    countries: { [number]: string },
    note: Note,
};

type NoteFeedBubbleState = {
    hover: boolean,
}

class NoteFeedBubble extends React.Component<NoteFeedBubbleProps, NoteFeedBubbleState> {

    constructor(props: NoteFeedBubbleProps) {
        super(props);
        this.state = {
            hover: false
        }
    }

    messageBox: ?HTMLDivElement;
    render(): React$Element<any> {
        return (
            <div className="message">
                <div
                    className="feedMessage"
                    onMouseOver={this._onMouseOver}
                    onMouseOut={this._onMouseOut}
                >
                    {this.props.note.msg}
                </div>
                {this.state.hover ? this.renderNoteInfo() : null}
            </div>
        );
    }

    renderNoteInfo: () => React$Element<any> = () => {
        const sender_name = this.props.note.sender ? this.props.countries[this.props.note.sender] : "Chair";
        const recipient_name = this.props.note.recipient ? this.props.countries[this.props.note.recipient] : "Chair";
        const timestamp = new Date(this.props.note.timestamp * 1000).toString();
        return (
            <div 
                classname="feedMessageInfo"
            >
            {sender_name} -> {recipient_name} : {timestamp}
            </div>
        );
    }

    _onMouseOver: (SyntheticEvent<any>) => void = (event) => {
        this.setState({ hover: true })
    }

    _onMouseOut: (SyntheticEvent<any>) => void = (event) => {
        this.setState({ hover: false })
    }
}

export { NoteFeedBubble };
