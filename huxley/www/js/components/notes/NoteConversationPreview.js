/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";
import type { Note } from "utils/types";

// $FlowFixMe
require("css/notes/NoteConversationPreview.less");
type NoteConversationPreviewProps = {
  recipient_name: ?string,
  country: string,
  last_message: ?Note,
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

  render(): React$Element<any> {
    const last_message_string = this.props.last_message
      ? this.props.last_message.msg
      : "";
    const textClass =
      this.props.country == this.props.recipient_name
        ? "countryNameSelected"
        : "countryName";
    const countryNameTruncated = this.props.country.length >= 20 
      ?  this.props.country.substring(0, 20).concat(`...`) 
      : this.props.country
        return (
      <div className="conversationPreview">
        <div className="conversationPreviewText">
          <div className={textClass}>{countryNameTruncated}</div>
          {last_message_string}
        </div>
      </div>
    );
  }
}

export { NoteConversationPreview };
