/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

require('whatwg-fetch');
var Cookie = require('js-cookie');

/**
 * The ServerAPI exists to centralize and abstract calls to the server. Any
 * code interacting with the server should go through this interface.
 */
var ServerAPI = {
  createDelegate(name, email, school) {
    return _post('/api/delegates', {name, email, school});
  },

  changePassword(currentPassword, newPassword) {
    return _put('/api/users/me/password', {
      password: currentPassword,
      new_password: newPassword,
    });
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
   * Get a list of all assignments for the given committee ID.
   */
  getCommitteeAssignments(committeeID) {
    return _get('/api/assignments/', {committee_id: committeeID});
  },

  /**
   * Get a list of all delegates for the given committee ID.
   */
  getCommitteeDelegates(committeeID) {
    return _get('/api/delegates/', {committee_id: committeeID});
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

  register(data) {
    return _post('/api/register', data);
  },

  resetPassword(username) {
    return _post('/api/users/me/password', {username});
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

  updateCommitteeDelegates(committeeID, delegates) {
    return _patch('/api/delegates', delegates);
  },

  updateUser(userID, data) {
    return _patch(`/api/users/${userID}`, data);
  },

  getRegistration(schoolID, conferenceID) {
    return _get('/api/registrations', {school_id: schoolID, conference_id: conferenceID});
  }
};

function _encodeQueryString(params) {
  return Object.entries(params)
    .map(e => encodeURIComponent(e[0]) + '=' + encodeURIComponent(e[1]))
    .join('&');
}

function _ajax(method, uri, data) {
  const isSafeMethod = /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  if (isSafeMethod && data) {
    uri = uri + '?' + _encodeQueryString(data);
  }
  const params = {
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
    },
    method: method,
  };
  if (!isSafeMethod) {
    params.headers['X-CSRFToken'] = Cookie.get('csrftoken');
    if (data) {
      params.body = typeof data === 'string' ? data : JSON.stringify(data);
    }
  }
  return fetch(uri, params).then(
    response =>
      response.ok
        ? response.json()
        : response.json().then(json => Promise.reject(json)),
  );
}

const _delete = _ajax.bind(null, 'DELETE');
const _get = _ajax.bind(null, 'GET');
const _patch = _ajax.bind(null, 'PATCH');
const _put = _ajax.bind(null, 'PUT');
const _post = _ajax.bind(null, 'POST');

module.exports = ServerAPI;
