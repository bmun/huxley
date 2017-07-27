/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

jest.dontMock("stores/CommitteeStore");

describe("CommitteeStore", () => {
  var ActionConstants;
  var CommitteeStore;
  var Dispatcher;
  var ServerAPI;

  var disc;
  var icj;
  var mockCommittees;
  var registerCallback;

  beforeEach(() => {
    ActionConstants = require("constants/ActionConstants");
    CommitteeStore = require("stores/CommitteeStore");
    Dispatcher = require("dispatcher/Dispatcher");
    ServerAPI = require("lib/ServerAPI");

    registerCallback = function(action) {
      Dispatcher.isDispatching.mockReturnValue(true);
      Dispatcher.register.mock.calls[0][0](action);
      Dispatcher.isDispatching.mockReturnValue(false);
    };

    disc = {id: 1, name: "DISC", special: false};
    icj = {id: 2, name: "ICJ", special: true};
    mockCommittees = [disc, icj];

    ServerAPI.getCommittees.mockReturnValue(Promise.resolve(mockCommittees));
  });

  it("subscribes to the dispatcher", () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it("requests the committees on first call and caches locally", () => {
    var committees = CommitteeStore.getCommittees();
    expect(committees).toEqual({});
    expect(ServerAPI.getCommittees).toBeCalled();

    registerCallback({
      actionType: ActionConstants.COMMITTEES_FETCHED,
      committees: mockCommittees,
    });

    committees = CommitteeStore.getCommittees();
    expect(Object.values(committees)).toEqual(mockCommittees);
    expect(ServerAPI.getCommittees.mock.calls.length).toEqual(1);
  });

  it("filters special committees", () => {
    registerCallback({
      actionType: ActionConstants.COMMITTEES_FETCHED,
      committees: mockCommittees,
    });

    var committees = CommitteeStore.getSpecialCommittees();
    expect(committees).toEqual({2: icj});
  });

  it("emits a change when the committees are loaded", function() {
    var callback = jest.genMockFunction();
    CommitteeStore.addListener(callback);
    expect(callback).not.toBeCalled();
    registerCallback({
      actionType: ActionConstants.COMMITTEES_FETCHED,
      committees: mockCommittees,
    });
    expect(callback).toBeCalled();
  });
});
