/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var PositionPaperActions = {
  fetchPositionPaperFile(fileName, paperID) {
    Dispatcher.dispatch({
      actionType: ActionConstants.FETCH_POSITION_PAPER_FILE,
      fileName: fileName,
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
};

module.exports = PositionPaperActions;
