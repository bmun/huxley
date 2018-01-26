/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var ActionConstants = require('constants/ActionConstants');
var Dispatcher = require('dispatcher/Dispatcher');

var RubricActions = {
  updateRubric(rubric, onSuccess, onError) {
    Dispatcher.dispatch({
      actionType: ActionConstants.UPDATE_RUBRIC,
      rubric: rubric,
      onSuccess: onSuccess,
      onError: onError
    });
  },

  rubricFetched(value) {
  	Dispatcher.dispatch({
      actionType: ActionConstants.RUBRIC_FETCHED,
      rubric: value,
    });
  }
};

module.exports = RubricActions;
