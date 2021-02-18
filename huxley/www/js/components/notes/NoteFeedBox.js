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
const { NoteFeedBubble } = require("components/notes/NoteFeedBubble");
const { NoteStore } = require("stores/NoteStore");

// $FlowFixMe
require("css/notes/NoteFeedBox.less");

type NoteFeedBoxProps = {
  countries: { [number]: string },
  notes: Note[],
};

class NoteFeedBox extends React.Component<NoteFeedBoxProps> {
  feedBox: ?HTMLDivElement;
  render(): React$Element<any> {
    return (
      <div
        className="feedBox"
        ref={(el) => {
          this.feedBox = el;
        }}
      >
        <div>
          {this.props.notes.map((note, index) => (
            <NoteFeedBubble
              note={note}
              key={index}
              countries={this.props.countries}
            />
          ))}
        </div>
      </div>
    );
  }

  componentDidMount() {
    if (this.feedBox) {
      this.feedBox.scrollTop = this.feedBox.scrollHeight;
    }
  }

  componentDidUpdate(prevProps: NoteFeedBoxProps) {
    if (this.props.notes.length !== prevProps.notes.length) {
      // TODO: find a way to make this number not arbitrary + not 
      // have issues if someone is scrolled all the way to the top
      if (
        this.feedBox &&
        (this.feedBox.scrollTop === 0 ||
          this.feedBox.scrollTop + 700 > this.feedBox.scrollHeight)
      ) {
        this.feedBox.scrollTop = this.feedBox.scrollHeight;
      }
    }
  }
}

export { NoteFeedBox };
