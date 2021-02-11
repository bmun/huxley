/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

/**
 * Checks if the current date falls within the range of February 28th to March 31st
 */
function _filterOnConversation(senderID, recipientID, chair, notes) {
    let noteIDs = [];
    if (chair) {
        console.log('test');
        noteIDs = Object.keys(notes).filter((noteID) =>
            (notes[noteID].sender == senderID && notes[noteID].is_chair == 2) ||
            (notes[noteID].is_chair == 1 && notes[noteID].recipient == senderID));
    } else {
        noteIDs = Object.keys(notes).filter((noteID) =>
            (notes[noteID].sender == senderID && notes[noteID].recipient == recipientID) ||
            (notes[noteID].sender == recipientID && notes[noteID].recipient == senderID));
    }

    return noteIDs.map(id => notes[id]);
}

function _getLastMessage(senderID, recipientID, chair, notes) {
    const conversation = _filterOnConversation(senderID, recipientID, chair)
    if (conversation.length > 0) {
        return conversation.sort((note1, note2) => note1.timestamp - note2.timestamp)[0]
    }
    return null;
}

export { _filterOnConversation, _getLastMessage };