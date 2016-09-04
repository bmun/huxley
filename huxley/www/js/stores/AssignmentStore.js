/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Dispatcher = require('dispatcher/Dispatcher');
var ServerAPI = require('lib/ServerAPI');
var {Store} = require('flux/utils');


var _assignmentPromises = {};

class AssignmentStore extends Store {
  getAssignments(schoolID, callback) {
    if (!_assignmentPromises[schoolID]) {
      _assignmentPromises[schoolID] = ServerAPI.getAssignments(schoolID);
    }
    if (callback) {
      _assignmentPromises[schoolID].then(callback);
    }
    return _assignmentPromises[schoolID];
  }

  __onDispatch(action) {
    // This method must be overwritten
    return;
  }
};

module.exports = new AssignmentStore(Dispatcher);
