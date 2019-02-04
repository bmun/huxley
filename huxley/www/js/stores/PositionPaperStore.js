/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var CurrentUserStore = require('stores/CurrentUserStore');
var PositionPaperActions = require('actions/PositionPaperActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');

var _graded = {};
var _files = {};
var _papers = {};
var _previousUserID = -1;

class PositionPaperStore extends Store {
  getPositionPaperFile(paperID) {
    if (paperID in _files) {
      return _files[paperID];
    } else {
      ServerAPI.getPositionPaperFile(paperID).then(value => {
        PositionPaperActions.positionPaperFileFetched(value, paperID);
      });

      return null;
    }
  }

  getGradedPositionPaperFile(paperID) {
    if (paperID in _graded) {
      return _graded[paperID];
    } else {
      ServerAPI.getGradedPositionPaperFile(paperID).then(value => {
        PositionPaperActions.gradedPositionPaperFileFetched(value, paperID);
      });
      return null;
    }
  }

  getPositionPaperFiles() {
    return _files;
  }

  getGradedPositionPaperFiles() {
    return _graded;
  }

  updatePositionPaper(paper, onSuccess, onError) {
    ServerAPI.updatePositionPaper(paper).then(onSuccess, onError);
  }

  uploadPaper(paper, file, onSuccess, onError) {
    _files[paper.id] = file;
    ServerAPI.uploadPositionPaper(paper, file).then(onSuccess, onError);
  }

  uploadGradedPaper(paper, file, onSuccess, onError) {
    _graded[paper.id] = file;
    ServerAPI.uploadGradedPositionPaper(paper, file).then(onSuccess, onError);
  }

  storePaper(paper) {
    _papers[paper.id] = paper;
  }

  getPapers() {
    return _papers;
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.FETCH_POSITION_PAPER_FILE:
        this.getPositionPaperFile(action.id);
        break;
      case ActionConstants.POSITION_PAPER_FILE_FETCHED:
        _files[action.id] = action.file;
        break;
      case ActionConstants.GRADED_POSITION_PAPER_FILE_FETCHED:
        _graded[action.id] = action.graded_file;
        break;
      case ActionConstants.UPDATE_POSITION_PAPER:
        this.updatePositionPaper(
          action.paper,
          action.onSuccess,
          action.onError,
        );
        break;
      case ActionConstants.UPLOAD_PAPER:
        delete _files[action.paper.id];
        if (action.paper.id in _papers) {
          _papers[action.paper.id] = action.paper;
        }
        this.uploadPaper(
          action.paper,
          action.file,
          action.onSuccess,
          action.onError,
        );
        break;
      case ActionConstants.UPLOAD_GRADED_PAPER:
        delete _graded[action.paper.id];
        if (action.paper.id in _papers) {
          _papers[action.paper.id] = action.paper;
        }
        this.uploadPaper(
          action.paper,
          action.graded_file,
          action.onSuccess,
          action.onError,
        );
        break;
      case ActionConstants.STORE_PAPER:
        this.storePaper(action.paper);
        break;
      case ActionConstants.ASSIGNMENTS_FETCHED:
        for (const assignment of action.assignments) {
          _papers[assignment.paper.id] = assignment.paper;
        }
        break;
      case ActionConstants.LOGIN:
        var userID = CurrentUserStore.getCurrentUser().id;
        if (userID != _previousUserID) {
          _papers = {};
          _previousUserID = userID;
        }
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

module.exports = new PositionPaperStore(Dispatcher);
