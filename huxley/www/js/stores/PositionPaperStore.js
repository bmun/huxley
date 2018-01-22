/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var PositionPaperActions = require('actions/PositionPaperActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');

var _files = {};
var _papersFetched = false;
var _previousUserID = -1;

class PositionPaperStore extends Store {
  getPositionPaperFile(paperID, fileName) {
    if (paperID in _files) {
      return _files[paperID]
    } else {
      ServerAPI.getPositionPaperFile(fileName).then(value => {
        PositionPaperActions.positionPaperFileFetched(value, paperID);
      });

      return null;
    }
  }

  getPositionPaperFiles() {
    return _files;
  }

  updatePositionPaper(paper, onSuccess, onError) {
    const paperCopy = {...paper};
    ServerAPI.updatePositionPaper(paperCopy).then(onSuccess, onError);
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.FETCH_POSITION_PAPER_FILE:
        this.getPositionPaperFile(action.id, action.fileName);
        break;
      case ActionConstants.POSITION_PAPER_FILE_FETCHED:
        _files[action.id] = action.file;
        break;
      case ActionConstants.UPDATE_POSITION_PAPER:
        this.updatePositionPaper(action.paper, action.onSuccess, action.onError);
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

module.exports = new PositionPaperStore(Dispatcher);