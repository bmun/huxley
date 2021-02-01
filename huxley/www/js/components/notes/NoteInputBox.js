/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

//@flow

'use strict';

import React from "react";
import type { Note } from "utils/types";

const { Button } = require('components/core/Button');
const { TextTemplate } = require('components/core/TextTemplate');
const { NoteActions } = require("actions/NoteActions");
const { NoteStore } = require('stores/NoteStore');
const { ServerAPI } = require("lib/ServerAPI");


type NoteInputBoxProps = {
    sender_id: ?number,
    recipient_id: ?number,
    is_chair: number
}

type NoteInputBoxState = {
    msg: ?string
}

class NoteInputBox extends React.Component<NoteInputBoxProps, NoteInputBoxState> {
    static defaultProps : NoteInputBoxProps = {
        sender_id: null,
        recipient_id: null,
        is_chair: 0
    }
    constructor(props : NoteInputBoxProps) {
        super(props);

        this.state = {
            msg: null
        }
    }

    render(): any {
        return (
            <div>
                <form onSubmit = {this._handleSubmit}>
                    <input 
                        className='noteInput' 
                        type="text" value={this.state.msg} 
                        onChange={this._handleChange} 
                        maxlength='1000'
                    />
                    <input type="submit" style={{"display": "none"}} />
                </form>
                <Button size = "small" onClick = {this._handleSubmit} color = "blue">Send</Button>
            </div>)
    }

    _handleChange: (any) => void = (event) => {
        this.setState({msg: event.target.value});
    }

    _handleSubmit: (any) => void = (event) => {
        if (this.state.msg) {
            const note: Note  = {
                sender_id: this.props.sender_id, 
                recipient_id: this.props.recipient_id,
                is_chair: this.props.is_chair,
                msg: this.state.msg
            }
            ServerAPI.createNote(
                note.is_chair, 
                note.sender_id, 
                note.recipient_id, 
                note.msg).then(this._handleNoteInputSuccess, this._handleNoteInputError);
        }
        event.preventDefault();
    }

    _handleNoteInputSuccess: (any) => void = (response) => {
        NoteActions.addNote(response);
        this.setState({msg: ''});
    }

    _handleNoteInputError: (any) => void = (response) => {
        window.alert(`Message was unable to be sent`);
        //TODO - fix this!
    }
}

export { NoteInputBox };
