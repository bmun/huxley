/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";

const { Button } = require("components/core/Button");

// $FlowFixMe
require("css/notes/NoteConversationPreview.less");
type NoteConversationPreviewProps = {
  country: string,
  last_message: any,
};

type NoteConversationPreviewState = {
  selected: ?string,
};

class NoteConversationPreview extends React.Component<
  NoteConversationPreviewProps,
  NoteConversationPreviewState
> {
  constructor(props: NoteConversationPreviewProps) {
    super(props);
    this.state = {
      selected: null,
    };
  }

  render(): any {
    let last_message_string = this.props.last_message
      ? this.props.last_message.msg
      : "";
    return (
      <div class="conversationPreview">
        <div class="conversationPreviewText">
          <div class="countryName">{this.props.country}</div>
          {last_message_string}
        </div>
      </div>
    );
  }
}

export { NoteConversationPreview };
