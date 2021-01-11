/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var CurrentUserStore = require('stores/CurrentUserStore');
var NoteActions = require('actions/NoteActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');

var _notes = {};
var _notesFetched = false;
var _previousUserID = -1;

class NoteStore extends Store {
  getCommitteeNotes(committeeID) {
    var noteIDs = Object.keys(_notes);
    if (!_notesFetched) {
      ServerAPI.getNotesByCommitteee(committeeID).then(value => {
        NoteActions.notesFetched(value);
      });

      return [];
    }

    return noteIDs.map(id => _notes[id]);
  }

  getConversationNotes(senderID, recipientID, chair) {
    var noteIDs = Object.keys(_notes);
    if (!_notesFetched) {
        if (chair) {
            ServerAPI.geteNotesByConversationWithChair(senderID).then(value => {
                NoteActions.notesFetched(value);
            });
        } else {
            ServerAPI.getNotesByConversation(senderID, recipientID).then(value => {
                NoteActions.notesFetched(value);
            });
        }

      return [];
    }

    return noteIDs.map(id => _notes[id]);
  }

  addNote(note) {
    _notes[note.id] = note;
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.ADD_NOTE:
        this.addNote(action.note);
        break;
      case ActionConstants.NOTES_FETCHED:
        for (const note of action.notes) {
          _notes[note.id] = note;
        }
        _notesFetched = true;
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

module.exports = new NoteStore(Dispatcher);
