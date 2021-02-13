/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

//@flow

import type { Note } from "utils/types";

/**
 * Checks if the current date falls within the range of February 28th to March 31st
 */
function _filterOnConversation(
  senderID: number,
  recipientID: ?number,
  chair: boolean,
  notes: Note[]
): Note[] {
  let noteIDs = [];
  if (chair && notes) {
    //$FlowFixMe flow is wrong and Object.keys can be called on an array (see MDN docs)
    noteIDs = Object.keys(notes).filter(
      (noteID) => {
        return (notes[noteID].sender == senderID && notes[noteID].is_chair == 2) ||
        (notes[noteID].is_chair == 1 && notes[noteID].recipient == senderID);}
    );
  } else if (recipientID && notes) {
    //$FlowFixMe flow is wrong and Object.keys can be called on an array (see MDN docs) 
    noteIDs = Object.keys(notes).filter(
      (noteID) =>
        (notes[noteID].sender == senderID &&
          notes[noteID].recipient == recipientID) ||
        (notes[noteID].sender == recipientID &&
          notes[noteID].recipient == senderID)
    );
  }

  return noteIDs.map((id) => notes[id]);
}

function _getLastMessage(
  senderID: number,
  recipientID: ?number,
  chair: boolean,
  notes: Note[]
): ?Note {
  const conversation = _filterOnConversation(
    senderID,
    recipientID,
    chair,
    notes
  );
  if (conversation.length > 0) {
    return conversation.sort((note1, note2) =>
      note1.timestamp && note2.timestamp ? note2.timestamp - note1.timestamp : 0
    )[0];
  }
  return null;
}

export { _filterOnConversation, _getLastMessage };
