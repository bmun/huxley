/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var RubricActions = require('actions/RubricActions');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');

var _rubrics = {};

class RubricStore extends Store {
  getRubric(rubricID) {
    if (rubricID in _rubrics) {
      return _rubrics[rubricID];
    } else {
      ServerAPI.getRubric(rubricID).then(value => {
        RubricActions.rubricFetched(value);
      });

      return null;
    }
  }

  updateRubric(rubric, onSuccess, onError) {
    ServerAPI.updateRubric(rubric).then(onSuccess, onError);
    _rubrics[rubric.id] = rubric;
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.RUBRIC_FETCHED:
        _rubrics[action.rubric.id] = action.rubric;
        break;
      case ActionConstants.UPDATE_RUBRIC:
        this.updateRubric(action.rubric, action.onSuccess, action.onError);
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

module.exports = new RubricStore(Dispatcher);
