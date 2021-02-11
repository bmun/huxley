/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";

const { Button } = require("components/core/Button");
const { NoteConversationPreview } = require("components/notes/NoteConversationPreview");

// $FlowFixMe
require("css/notes/NoteConversationSelector.less");
type NoteSidebarProps = {
  assignments: { [string]: any },
  last_messages: { [string]: any },
  onConversationChange: (any) => void,
  onChairConversationChange: () => void,
};

type NoteSidebarState = {
  selected: ?string,
};

class NoteSidebar extends React.Component<
  NoteSidebarProps,
  NoteSidebarState
> {
  constructor(props: NoteSidebarProps) {
    super(props);
    this.state = {
      selected: null,
    };
  }

  render(): any {
    return (
       Object.keys(this.props.assignments).map((country) => <div onClick={(event) => this._handleClick(event, country)}><NoteConversationPreview country = {country} last_message = {this.props.last_messages[country]}/></div>)
    );
  }

  _handleClick: (SyntheticEvent<HTMLInputElement>, string) => void = (event, country) => {
    if (country === "Chair") {
      this.props.onChairConversationChange();
    } else if (country in this.props.assignments) { 
      this.props.onConversationChange(this.props.assignments[country]);
    }
  };
}

export { NoteSidebar };
