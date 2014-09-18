/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var $ = require('jquery');
var Promise = require('es6-promise').Promise;


var _assignmentPromise = null;

var AssignmentStore = {
  getAssignments: function(schoolID, callback) {
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

    _assignmentPromise.then(callback);
  },
};

module.exports = AssignmentStore;
