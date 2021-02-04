/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

 //@flow 

 'use strict';

import React from "react";

const { Button } = require('components/core/Button');

type NoteConversationSelectorProps = {
    assignments: {[string]: any},
    onConversationChange: (any) => void,
    onChairConversationChange: () => void
}

type NoteConversationSelectorState = {
    selected: ?string
}

class NoteConversationSelector extends React.Component<NoteConversationSelectorProps, NoteConversationSelectorState> {
    
    constructor(props : NoteConversationSelectorProps) {
        super(props);
        console.log(this.props.assignments)
        this.state = {
            selected: null
        }
    }

    render() : any {
        return ( 
            <div>
                <form onSubmit = {this._handleSubmit}>
                    <datalist id="delegations">
                        <option>Chair</option>
                        {Object.keys(this.props.assignments).map(country => <option>{country}</option>)}
                    </datalist>
                    <input  autoComplete="on" list="delegations" onChange = {this._handleChange}/> 
                    <input type= "submit" style = {{"display": "none"}}/>
                </form>
                <Button size = "small" onClick = {this._handleSubmit} color = "blue">&#10140;</Button>
            </div> )
    }

    _handleChange: (any) => void = (event) => {
        this.setState({selected: event.target.value});
    }

    _handleSubmit: (any) => void = (event) => {
        if (this.state.selected && this.state.selected === "Chair") {
            this.props.onChairConversationChange()
        } else if (this.state.selected && this.state.selected in this.props.assignments) {
            this.props.onConversationChange(this.props.assignments[this.state.selected])
        }
        event.preventDefault();
    }

}

export { NoteConversationSelector }