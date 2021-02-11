/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";

const { Button } = require("components/core/Button");
const {
  NoteConversationPreview,
} = require("components/notes/NoteConversationPreview");

// $FlowFixMe
require("css/notes/NoteSidebar.less");
type NoteSidebarProps = {
  recipient_name: string,
  assignments: { [string]: any },
  last_messages: { [string]: any },
  onConversationChange: (any) => void,
  onChairConversationChange: () => void,
};

type NoteSidebarState = {
  selected: ?string,
};

class NoteSidebar extends React.Component<NoteSidebarProps, NoteSidebarState> {
  constructor(props: NoteSidebarProps) {
    super(props);
    this.state = {
      selected: null,
    };
  }

  render(): any {
    const sorted_countries = Object.keys(this.props.last_messages).sort(
      (country1, country2) => {
        return (
          (this.props.last_messages[country2]
            ? this.props.last_messages[country2].timestamp
            : 0) -
          (this.props.last_messages[country1]
            ? this.props.last_messages[country1].timestamp
            : 0)
        );
      }
    );
    return (
      <div className="sidebar">
        {sorted_countries.map((country) => (
          <div key={country} onClick={(event) => this._handleClick(event, country)}>
            <NoteConversationPreview
              recipient_name={this.props.recipient_name}
              country={country}
              last_message={this.props.last_messages[country]}
            />
          </div>
        ))}
      </div>
    );
  }

  _handleClick: (SyntheticEvent<HTMLInputElement>, string) => void = (
    event,
    country
  ) => {
    if (country === "Chair") {
      this.props.onChairConversationChange();
    } else if (country in this.props.assignments) {
      this.props.onConversationChange(this.props.assignments[country]);
    }
  };
}

export { NoteSidebar };
