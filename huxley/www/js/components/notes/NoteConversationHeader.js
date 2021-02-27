/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";
import type { Note } from "utils/types";

const { Button } = require("components/core/Button");

type NoteConversationHeaderProps = {
  recipient_name?: ?string,
  onRefreshNotes: () => void,
};

class NoteConversationHeader extends React.Component<NoteConversationHeaderProps> {
  render(): React$Element<any> {
    return (
      <h1>
        {this.props.recipient_name}{this.props.recipient_name ? " " : ""}
        <Button size="small" onClick={this.props.onRefreshNotes} color="green" style={{marginLeft: "10px"}}>
          Refresh
        </Button>
      </h1>
    );
  }
}

export { NoteConversationHeader };
