/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

//@flow

'use strict';

import React from "react";

const { Button } = require('components/core/Button');
const { TextTemplate } = require('components/core/TextTemplate');
const { NoteStore } = require('stores/NoteStore');


type NoteInputBoxProps = {
    sender_id: ?number,
    recipient_id: ?number,
    chair: number
}

type NoteInputBoxState = {
    msg: ?string
}

class NoteInputBox extends React.Component<NoteInputBoxProps, NoteInputBoxState> {

    constructor(props : NoteInputBoxProps) {
        super(props);

        this.state = {
            msg: null
        }
    }

    render(): any {
        return <input 
                    className='noteInput' 
                    type="text" value={this.state.msg} 
                    onChange={this.handleChange} 
                    maxlength='1000'
                />
    }

    handleChange = (event : any) : void => {
        this.setState({msg: event.target.value});
    }

    handleSubmit = (event : any) : void => {
        if (this.state.msg) {

        }
        NoteStore.addNote()
    }

}

export { NoteInputBox };
