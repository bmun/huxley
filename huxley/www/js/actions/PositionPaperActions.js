/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var PositionPaperActions = {
  fetchPositionPaperFile(paperID) {
    Dispatcher.dispatch({
      actionType: ActionConstants.FETCH_POSITION_PAPER_FILE,
      id: paperID,
    });
  },

  positionPaperFileFetched(file, paperID) {
    Dispatcher.dispatch({
      actionType: ActionConstants.POSITION_PAPER_FILE_FETCHED,
      file: file,
      id: paperID,
    });
  },

  updatePositionPaper(paper, onSuccess, onError) {
    Dispatcher.dispatch({
      actionType: ActionConstants.UPDATE_POSITION_PAPER,
      paper: paper,
      onSuccess: onSuccess,
      onError: onError,
    });
  },

  storePositionPaper(paper) {
    Dispatcher.dispatch({
      actionType: ActionConstants.STORE_PAPER,
      paper: paper,
    });
  },

  uploadPaper(paper, file, onSuccess, onError) {
    Dispatcher.dispatch({
      actionType: ActionConstants.UPLOAD_PAPER,
      paper: paper,
      file: file,
      onSuccess: onSuccess,
      onError: onError,
    });
  },
};

module.exports = PositionPaperActions;
