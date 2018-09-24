/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/SecretariatMemberStore');

describe('SecretariatMemberStore', () => {
  var ActionConstants;
  var SecretariatMemberStore;
  var Dispatcher;
  var ServerAPI;

  var mockSecretariatMembers;
  var mockCommitteeID;
  var noSecretariatMemberCommitteeID;
  var registerCallback;

  beforeEach(() => {
    ActionConstants = require('constants/ActionConstants');
    SecretariatMemberStore = require('stores/SecretariatMemberStore');
    Dispatcher = require('dispatcher/Dispatcher');
    ServerAPI = require('lib/ServerAPI');

    registerCallback = function(action) {
      Dispatcher.isDispatching.mockReturnValue(true);
      Dispatcher.register.mock.calls[0][0](action);
      Dispatcher.isDispatching.mockReturnValue(false);
    };

    mockCommitteeID = 1;
    noSecretariatMemberCommitteeID = 0;

    var mockSecretariatMember1 = {
      id: 1,
      name: 'Tomato King',
      committee: mockCommitteeID,
      is_head_chair: true,
    };

    var mockSecretariatMember2 = {
      id: 2,
      name: 'Fruit Hero',
      committee: mockCommitteeID,
      is_head_chair: false,
    };

    mockSecretariatMembers = [mockSecretariatMember1, mockSecretariatMember2];

    ServerAPI.getSecretariatMembers.mockReturnValue(
      Promise.resolve(mockSecretariatMembers),
    );
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the secretariat members on the first call and caches locally', () => {
    var secretariatMembers = SecretariatMemberStore.getSecretariatMembers(
      mockCommitteeID,
    );
    expect(secretariatMembers.length).toEqual(0);
    expect(ServerAPI.getSecretariatMembers).toBeCalledWith(mockCommitteeID);

    registerCallback({
      actionType: ActionConstants.SECRETARIAT_MEMBERS_FETCHED,
      secretariatMembers: mockSecretariatMembers,
    });

    secretariatMembers = SecretariatMemberStore.getSecretariatMembers(
      mockCommitteeID,
    );
    expect(secretariatMembers).toEqual(mockSecretariatMembers);
    expect(ServerAPI.getSecretariatMembers.mock.calls.length).toEqual(1);
  });

  it('differentiates no secretariat members from not having fetched secretariat members', () => {
    var secretariatMembers = SecretariatMemberStore.getSecretariatMembers(
      noSecretariatMemberCommitteeID,
    );
    expect(secretariatMembers.length).toEqual(0);
    expect(ServerAPI.getSecretariatMembers).toBeCalledWith(
      noSecretariatMemberCommitteeID,
    );

    registerCallback({
      actionType: ActionConstants.SECRETARIAT_MEMBERS_FETCHED,
      secretariatMembers: [],
    });

    secretariatMembers = SecretariatMemberStore.getSecretariatMembers(
      noSecretariatMemberCommitteeID,
    );
    expect(secretariatMembers).toEqual([]);
    expect(ServerAPI.getSecretariatMembers.mock.calls.length).toEqual(1);
  });

  it('emits a change when the secretariat members is loaded', () => {
    var callback = jest.genMockFunction();
    SecretariatMemberStore.addListener(callback);
    expect(callback).not.toBeCalled();
    registerCallback({
      actionType: ActionConstants.SECRETARIAT_MEMBERS_FETCHED,
      secretariatMembers: mockSecretariatMembers,
    });
    expect(callback).toBeCalled();
  });
});
