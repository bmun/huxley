/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Dispatcher = require('dispatcher/Dispatcher');
var {Store} = require('flux/utils');


var _assignmentPromise = null;

class AssignmentStore extends Store {
  getAssignments(schoolID, callback) {
    if (!_assignmentPromise) {
      _assignmentPromise = new Promise(function(resolve, reject) {
        $.ajax({
          type: 'GET',
          url: '/api/schools/'+schoolID+'/assignments',
          dataType: 'json',
          success: function(data, textStatus, jqXHR) {
            resolve(jqXHR.responseJSON);
          },
        });
      });
    }

    if (callback) {
      _assignmentPromise.then(callback);
    }
    return _assignmentPromise;
  }

  __onDispatch(action) {
    // This method must be overwritten
    return;
  }
};

module.exports = new AssignmentStore(Dispatcher);
