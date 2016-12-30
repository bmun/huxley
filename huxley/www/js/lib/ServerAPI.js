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
  createDelegate(name, email, school) {
    return _post('/api/delegates', {name, email, school});
  },

  deleteDelegate(delegateID) {
    return _delete(`/api/delegates/${delegateID}`);
  },

  /**
   * Get a list of all assignments for the given school ID.
   */
  getAssignments(schoolID) {
    return _get('/api/assignments', {school_id: schoolID});
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
    return _get('/api/delegates', {school_id: schoolID});
  },

  login(username, password) {
    return _post('/api/users/me', {username, password});
  },

  logout() {
    return _delete('/api/users/me');
  },

  updateAssignment(assignmentID, data) {
    return _patch(`/api/assignments/${assignmentID}`, data);
  },

  updateDelegate(delegateID, data) {
    return _patch(`/api/delegates/${delegateID}`, data);
  },

  updateSchool(schoolID, data) {
    return _patch(`/api/schools/${schoolID}`, data);
  },

  updateSchoolDelegates(schoolID, delegates) {
    return _patch('/api/delegates', delegates);
  },
};

function _ajax(method, uri, data) {
  return new Promise((resolve, reject) => {
    $.ajax({
      type: method,
      url: uri,
      contentType: 'application/json; charset=UTF-8',
      data: typeof data === 'string' ? data : JSON.stringify(data),
      dataType: 'json',
      success: (data, textStatus, jqXHR) => {
        resolve(jqXHR.responseJSON);
      },
      error: (jqXHR, status, error) => {
        reject(jqXHR.responseJSON);
      },
    });
  });
}

const _delete = _ajax.bind(null, 'DELETE');
const _get = _ajax.bind(null, 'GET');
const _patch = _ajax.bind(null, 'PATCH');
const _post = _ajax.bind(null, 'POST');

$.ajaxSetup({
  beforeSend: (xhr, settings) => {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
      // TODO: check that it's same origin.
      xhr.setRequestHeader('X-CSRFToken', Cookie.get('csrftoken'));
    }
  },
});

module.exports = ServerAPI;
