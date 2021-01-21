/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import ActionConstants from 'constants/ActionConstants';
import { CurrentUserStore } from "stores/CurrentUserStore";
import { NoteActions } from "actions/NoteActions";
import { Dispatcher } from "dispatcher/Dispatcher";
import { ServerAPI } from "lib/ServerAPI";
import { Store } from "flux/utils";

var _notes = {};
var _notesFetched = false;
var _previousUserID = -1;

class NoteStore extends Store {
  getCommitteeNotes(committeeID) {
    var noteIDs = Object.keys(_notes);
    if (!_notesFetched) {
      ServerAPI.getNotesByCommitteee(committeeID).then(value => 
        NoteActions.notesFetched(value)
      );

      return [];
    }

    return noteIDs.map(id => _notes[id]);
  }

  getConversationNotes(senderID, recipientID, chair) {
    var noteIDs = Object.keys(_notes);
    if (!_notesFetched) {
        if (chair) {
            ServerAPI.getNotesByConversationWithChair(senderID).then(value => 
                NoteActions.notesFetched(value)
            );
        } else {
            ServerAPI.getNotesByConversation(senderID, recipientID).then(value => 
                NoteActions.notesFetched(value)
            );
        }

      return [];
    }

    return noteIDs.map(id => _notes[id]);
  }

  addNote(note) {
    _notes[note.id] = note;
    ServerAPI.createNote(note.is_chair, note.sender, note.recipient, note.msg);
  }

  __onDispatch(action) {
    console.log(action.actionType);
    switch (action.actionType) {
      case ActionConstants.ADD_NOTE:
        console.log('action constant was add note');
        this.addNote(action.note);
        break;
      case ActionConstants.NOTES_FETCHED:
        for (const note of action.notes) {
          _notes[note.id] = note;
        }
        console.log(_notes);
        _notesFetched = true;
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

const noteStore = new NoteStore(Dispatcher);
export { noteStore as NoteStore };
