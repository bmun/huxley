/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/RegistrationStore');

describe('RegistrationStore', () => {
  var ActionConstants;
  var Dispatcher;
  var RegistrationStore;
  var ServerAPI;

  var registerCallback;
  var mockSchoolID;
  var mockConferenceID;
  var mockRegistration;

  beforeEach(function() {
    ActionConstants = require('constants/ActionConstants');
    Dispatcher = require('dispatcher/Dispatcher');
    {RegistrationStore} = require('stores/RegistrationStore');
    ServerAPI = require('lib/ServerAPI');

    registerCallback = function(action) {
      Dispatcher.isDispatching.mockReturnValue(true);
      Dispatcher.register.mock.calls[0][0](action);
      Dispatcher.isDispatching.mockReturnValue(false);
    };
    mockSchoolID = 1;
    mockConferenceID = 65;
    mockRegistration = {
      id: 1,
      school: mockSchoolID,
      conference: mockConferenceID,
      assignments_finalized: false,
    };

    ServerAPI.getRegistration.mockReturnValue(
      Promise.resolve(mockRegistration),
    );
    ServerAPI.updateRegistration.mockReturnValue(Promise.resolve({}));
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the registration on first call and caches locally', () => {
    var registration = RegistrationStore.getRegistration(
      mockSchoolID,
      mockConferenceID,
    );
    expect(ServerAPI.getRegistration).toBeCalled();

    registerCallback({
      actionType: ActionConstants.REGISTRATION_FETCHED,
      registration: mockRegistration,
    });

    registration = RegistrationStore.getRegistration(
      mockSchoolID,
      mockConferenceID,
    );
    expect(registration).toEqual(mockRegistration);
    expect(ServerAPI.getRegistration.mock.calls.length).toEqual(1);
  });

  it('emits a change when the registration is loaded', function() {
    var callback = jest.genMockFunction();
    RegistrationStore.addListener(callback);
    expect(callback).not.toBeCalled();
    registerCallback({
      actionType: ActionConstants.REGISTRATION_FETCHED,
      delegates: mockRegistration,
    });
    expect(callback).toBeCalled();
  });

  it('updates the registration and emits a change', () => {
    registerCallback({
      actionType: ActionConstants.REGISTRATION_FETCHED,
      registration: mockRegistration,
    });

    var callback = jest.genMockFunction();
    RegistrationStore.addListener(callback);
    expect(callback).not.toBeCalled();

    var delta = {assignments_finalized: true};
    registerCallback({
      actionType: ActionConstants.UPDATE_REGISTRATION,
      registrationID: 1,
      delta: delta,
      onError: jest.genMockFunction(),
    });
    expect(callback).toBeCalled();

    var registration = RegistrationStore.getRegistration(
      mockSchoolID,
      mockConferenceID,
    );
    expect(ServerAPI.updateRegistration).toBeCalledWith(1, registration);
    expect(registration.assignments_finalized).toEqual(
      delta.assignments_finalized,
    );
  });
});
