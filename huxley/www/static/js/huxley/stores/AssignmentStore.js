/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');

var _assignmentRequest = null;

var AssignmentStore = {
  getAssignments: function(schoolID, callback) {
    if (!_assignmentRequest) {
      _assignmentRequest = $.ajax({
        type: 'GET',
        url: '/api/schools/'+schoolID+'/assignments',
        dataType: 'json'
      });
    }
    _assignmentRequest.done(function(data, textStatus, jqXHR) {
      callback(jqXHR.responseJSON);
    });
  }
};

module.exports = AssignmentStore;
