/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */
//@flow

'use strict';

import ActionConstants from 'constants/ActionConstants';
import { CurrentUserStore } from "stores/CurrentUserStore";
import { NoteActions } from "actions/NoteActions";
import { Dispatcher } from "dispatcher/Dispatcher";
import { ServerAPI } from "lib/ServerAPI";
import { Store } from "flux/utils";

import type {Note} from 'utils/types';


let _notes: {[string]: Note} = {};
let _lastFetchedTimestamp = 0;
let _noteCheckpointTimestamp = 0;
let _previousUserID = -1;
const PollingInterval = global.conference.polling_interval;
const MaxRefreshInterval = global.conference.max_refresh_interval;
const NoteCheckpointPadding = global.conference.note_checkpoint_padding;
const _refreshInterval = (PollingInterval / 2 < MaxRefreshInterval) ? PollingInterval / 2 : MaxRefreshInterval;

class NoteStore extends Store {
  getCommitteeNotes(committeeID: number): Note[] {
    let noteIDs = Object.keys(_notes);
    if (_lastFetchedTimestamp < Date.now() - _refreshInterval) { 
      _lastFetchedTimestamp = Date.now() - 10;
      ServerAPI.getNotesByCommittee(committeeID, _noteCheckpointTimestamp).then(value => 
        NoteActions.notesFetched(value)
      );
    }

    return noteIDs.map(id => _notes[id]);
  }

  getConversationNotes(senderID: number): Note[] {
    let noteIDs = Object.keys(_notes);;
    if (_lastFetchedTimestamp < Date.now() - _refreshInterval) {
      _lastFetchedTimestamp = Date.now() - 10;
      ServerAPI.getNotesBySender(senderID, _noteCheckpointTimestamp).then(value => 
        NoteActions.notesFetched(value));
    }
    return noteIDs.map(id => _notes[id]);
  }

  addNote(note: Note): void {
    _notes[note.id.toString()] = note;
  }

  __onDispatch(action: any): void {
    switch (action.actionType) {
      case ActionConstants.ADD_NOTE:
        this.addNote(action.note);
        break;
      case ActionConstants.NOTES_FETCHED:
        for (const note of action.notes) {
          _notes[note.id] = note;
        }
        // subtracting half of polling period to ensure that no notes are missed in the time it takes the server to communicate with the client
        //IF this is too big, bad for bandwith, if too small, delegates won't see notes.
        _noteCheckpointTimestamp = Date.now() - NoteCheckpointPadding; 
        break;
      case ActionConstants.LOGIN:
        var userID = CurrentUserStore.getCurrentUser().id;
        if (userID != _previousUserID) {
          _notes = {};
          _lastFetchedTimestamp = 0;
          _previousUserID = userID;
        }
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

const noteStore: NoteStore = new NoteStore(Dispatcher);
export { noteStore as NoteStore };
