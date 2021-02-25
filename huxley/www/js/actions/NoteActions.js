/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import ActionConstants from 'constants/ActionConstants';
import {Dispatcher} from 'dispatcher/Dispatcher';

var NoteActions = {
  addNote(note) {
    Dispatcher.dispatch({
      actionType: ActionConstants.ADD_NOTE,
      note: note,
    });
  },

  notesFetched(notes) {
    Dispatcher.dispatch({
      actionType: ActionConstants.NOTES_FETCHED,
      notes: notes,
    });
  },
};

export { NoteActions };
