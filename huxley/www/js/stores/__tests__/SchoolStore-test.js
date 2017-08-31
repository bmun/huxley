/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/SchoolStore');

describe('SchoolStore', () => {
  var ActionConstants;
  var SchoolStore;
  var Dispatcher;
  var ServerAPI;

  var mockSchool;
  var mockSchoolID2;
  var registerCallback;

  beforeEach(() => {
    ActionConstants = require('constants/ActionConstants');
    SchoolStore = require('stores/SchoolStore');
    Dispatcher = require('dispatcher/Dispatcher');
    ServerAPI = require('lib/ServerAPI');

    registerCallback = function(action) {
      Dispatcher.isDispatching.mockReturnValue(true);
      Dispatcher.register.mock.calls[0][0](action);
      Dispatcher.isDispatching.mockReturnValue(false);
    };

    mockSchool = {
      id: 1,
      name: 'UC Berkeley',
      address: '2700 Hearst Ave.',
      city: 'Berkeley',
      state: 'CA',
      zip: 94720,
      country: 'United States of America',
      primary_name: 'Michael McDonald',
      primary_gender: 'Male',
      primary_phone: '(000) 000-0000',
      primary_type: 0,
      times_attended: 2,
      international: false
    };

    mockSchoolID2 = 3;

    ServerAPI.getSchool.mockReturnValue(Promise.resolve(mockSchool));
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the school on first call and caches locally', () => {
    var school = SchoolStore.getSchool(mockSchool.id);
    expect(school).toEqual(null);
    expect(ServerAPI.getSchool).toBeCalledWith(mockSchool.id);

    registerCallback({
      actionType: ActionConstants.SCHOOLS_FETCHED,
      schools: [mockSchool],
    });

    school = SchoolStore.getSchool(mockSchool.id);
    expect(school).toEqual(mockSchool);
    expect(ServerAPI.getSchool.mock.calls.length).toEqual(1);
  });

  it('differentiates no school from not having fetched a school', () => {
    var school = SchoolStore.getSchool(mockSchoolID2);
    expect(school).toEqual(null);
    expect(ServerAPI.getSchool).toBeCalledWith(mockSchoolID2);

    registerCallback({
      actionType: ActionConstants.SCHOOLS_FETCHED,
      schools: [],
    });

    school = SchoolStore.getSchool(mockSchoolID2);
    expect(school).toEqual(null);
    expect(ServerAPI.getSchool.mock.calls.length).toEqual(1);
  });

  it('emits a change when the school is loaded', function() {
    var callback = jest.genMockFunction();
    SchoolStore.addListener(callback);
    expect(callback).not.toBeCalled();
    registerCallback({
      actionType: ActionConstants.SCHOOLS_FETCHED,
      schools: [mockSchool],
    });
    expect(callback).toBeCalled();
  });
});
