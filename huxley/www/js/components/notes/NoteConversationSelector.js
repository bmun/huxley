/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";

const { Button } = require("components/core/Button");

// $FlowFixMe
require("css/notes/NoteConversationSelector.less");
type NoteConversationSelectorProps = {
  assignments: { [string]: any },
  onConversationChange: (any) => void,
  onChairConversationChange: () => void,
};

type NoteConversationSelectorState = {
  selected: ?string,
};

class NoteConversationSelector extends React.Component<
  NoteConversationSelectorProps,
  NoteConversationSelectorState
> {
  constructor(props: NoteConversationSelectorProps) {
    super(props);
    this.state = {
      selected: null,
    };
  }

  render(): any {
    return (
      <div class = "selector">
        <form onSubmit={this._handleSubmit}>
          <datalist id="delegations">
            <option>Chair</option>
            {Object.keys(this.props.assignments).map((country) => (
              <option>{country}</option>
            ))}
          </datalist>
          <input
            class="countrySelect"
            autoComplete="on"
            value={this.state.selected}
            list="delegations"
            onChange={this._handleChange}
          />
          <input type="submit" style={{ display: "none" }} />
        </form>
        <Button
          class="selectConversation"
          size="small"
          onClick={this._handleSubmit}
          color="blue"
        >
          &#10140;
        </Button>
      </div>
    );
  }

  _handleChange: (SyntheticEvent<HTMLInputElement>) => void = (event) => {
    /* Note: This feels hacky, possibly because it is. However, this seems to be the best way
        determine if a change was a click on a datalist element or typing by the user.
        See https://stackoverflow.com/questions/43898967/creating-onclick-event-for-datalist-option-in-react
        and https://stackoverflow.com/questions/31901351/how-to-fire-an-event-on-clicking-data-list-option-list 
        Currently does not work on Firefox; may be better to use a keydown event instead. */
    if (event.target instanceof HTMLInputElement) {
      this.setState({ selected: event.target.value }, () => {
        if (!(event.nativeEvent instanceof InputEvent)) {
          this._handleSubmit(event);
        }
      });
    }
  };

  _handleSubmit: (SyntheticEvent<HTMLInputElement>) => void = (event) => {
    if (this.state.selected && this.state.selected === "Chair") {
      this.props.onChairConversationChange();
      this.setState({ selected: "" });
    } else if (
      this.state.selected &&
      this.state.selected in this.props.assignments
    ) { // TODO: make this if case work if the user uses lowercase
      this.props.onConversationChange(
        this.props.assignments[this.state.selected]
      );
      this.setState({ selected: "" });
    }
    event.preventDefault();
  };
}

export { NoteConversationSelector };
