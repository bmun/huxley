/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import ActionConstants from "constants/ActionConstants";
import { RubricActions } from "actions/RubricActions";
import { Dispatcher } from "dispatcher/Dispatcher";
import { ServerAPI } from "lib/ServerAPI";
import { Store } from "flux/utils";

var _rubrics = {};

class RubricStore extends Store {
  getRubric(rubricID) {
    if (rubricID in _rubrics) {
      return _rubrics[rubricID];
    } else {
      ServerAPI.getRubric(rubricID).then((value) => {
        RubricActions.rubricFetched(value);
      });

      return null;
    }
  }

  updateRubric(rubric, onSuccess, onError) {
    _rubrics[rubric.id] = rubric;
    ServerAPI.updateRubric(rubric).then(onSuccess, onError);
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

const rubricStore = new RubricStore(Dispatcher);
export { rubricStore as RubricStore };
