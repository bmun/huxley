/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

var $ = require('jquery');
var Cookie = require('js-cookie');

/**
 * The ServerAPI exists to centralize and abstract calls to the server. Any
 * code interacting with the server should go through this interface.
 */
var ServerAPI = {
  /**
   * Get a list of all assignments for the given school ID.
   */
  getAssignments(schoolID) {
    return _get(`/api/schools/${schoolID}/assignments`);
  },

  /**
   * Get a list of all committees.
   */
  getCommittees() {
    return _get('/api/committees');
  },

  /**
   * Get a list of all countries.
   */
  getCountries() {
    return _get('/api/countries');
  },

  /**
   * Get a list of all delegates for the given school ID.
   */
  getDelegates(schoolID) {
    return _get(`/api/schools/${schoolID}/delegates`);
  },
};

function _get(uri) {
  return new Promise((resolve, reject) => {
    $.ajax({
      type: 'GET',
      url: uri,
      dataType: 'json',
      success: (data, textStatus, jqXHR) => {
        resolve(jqXHR.responseJSON);
      },
    });
  });
}

$.ajaxSetup({
  beforeSend: (xhr, settings) => {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
      // TODO: check that it's same origin.
      xhr.setRequestHeader('X-CSRFToken', Cookie.get('csrftoken'));
    }
  },
});

module.exports = ServerAPI;
