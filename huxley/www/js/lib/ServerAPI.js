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

  createCommitteeFeedback(feedback) {
    return _post(`/api/committee_feedback/post`, feedback);
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

  getCommitteeFeedback(committeeID) {
    return _get('/api/committee_feedback/', {committee_id: committeeID});
  },

  getSecretariatMember(secretariatMemberID) {
    return _get(`/api/secretariat_member/${secretariat_member}`);
  },

  getSecretariatMembers() {
    return _get('/api/secretariat_member');
  },

  getSecretariatMembers(committeeID) {
    return _get('/api/secretariat_member_committee/', {
      committee_id: committeeID,
    });
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

  resetDelegatePassword(delegateID) {
    return _post('/api/users/delegate/password', {delegate_id: delegateID});
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
    return _get('/api/registrations', {
      school_id: schoolID,
      conference_id: conferenceID,
    });
  },

  updateRegistration(registrationID, data) {
    return _patch(`/api/registrations/${registrationID}`, data);
  },

  getPositionPaperFile(paperID) {
    return _get(
      '/api/papers/file',
      {id: paperID},
      'application/force-download',
    );
  },

  updatePositionPaper(paper) {
    return _patch(`api/papers/${paper.id}`, paper);
  },

  uploadPositionPaper(paper, file) {
    return _post(`api/papers/${paper.id}`, {file: file}, 'multipart/form-data');
  },

  getRubric(rubricID) {
    return _get(`api/rubrics/${rubricID}`);
  },

  updateRubric(rubric) {
    return _patch(`api/rubrics/${rubric.id}`, rubric);
  },
};

function _encodeQueryString(params) {
  return Object.entries(params)
    .map(e => encodeURIComponent(e[0]) + '=' + encodeURIComponent(e[1]))
    .join('&');
}

function _ajax(method, uri, data, content_type) {
  if (content_type == null) {
    content_type = 'application/json';
  }

  const isSafeMethod = /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  if (isSafeMethod && data) {
    uri = uri + '?' + _encodeQueryString(data);
  }
  var params = {};
  if (content_type == 'application/json') {
    params = {
      credentials: 'same-origin',
      headers: {
        'Content-Type': `${content_type}`,
      },
      method: method,
    };
  } else {
    params = {
      credentials: 'same-origin',
      headers: {},
      method: method,
    };
  }

  if (!isSafeMethod) {
    params.headers['X-CSRFToken'] = Cookie.get('csrftoken');
    if (data && content_type != 'multipart/form-data') {
      params.body = typeof data === 'string' ? data : JSON.stringify(data);
    } else if (data && content_type == 'multipart/form-data') {
      var form = new FormData();
      form.append('file', data['file']);
      params.body = form;
    }
  }

  if (content_type == 'application/json') {
    return fetch(uri, params).then(
      response =>
        response.ok
          ? response.json()
          : response.json().then(json => Promise.reject(json)),
    );
  } else if (content_type == 'application/force-download') {
    return fetch(uri, params).then(
      response =>
        response.ok
          ? response.blob()
          : response.blob().then(json => Promise.reject(json)),
    );
  } else {
    return fetch(uri, params).then(
      response =>
        response.ok
          ? response.text()
          : response.text().then(text => Promise.reject(text)),
    );
  }
}

const _delete = _ajax.bind(null, 'DELETE');
const _get = _ajax.bind(null, 'GET');
const _patch = _ajax.bind(null, 'PATCH');
const _put = _ajax.bind(null, 'PUT');
const _post = _ajax.bind(null, 'POST');

module.exports = ServerAPI;
