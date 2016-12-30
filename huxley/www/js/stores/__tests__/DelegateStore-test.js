/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/DelegateStore');

describe('DelegateStore', () => {
  var ActionConstants;
  var DelegateStore;
  var Dispatcher;
  var ServerAPI;

  var jake, nate
  var mockDelegates, mockSchoolID;
  var registerCallback;

  beforeEach(() => {
    ActionConstants = require('constants/ActionConstants');
    DelegateStore = require('stores/DelegateStore');
    Dispatcher = require('dispatcher/Dispatcher');
    ServerAPI = require('lib/ServerAPI');

    registerCallback = function(action) {
      Dispatcher.isDispatching.mockReturnValue(true);
      Dispatcher.register.mock.calls[0][0](action);
      Dispatcher.isDispatching.mockReturnValue(false);
    };

    mockSchoolID = 1;
    jake = {id: 1, name: 'Jake', email: '', school: mockSchoolID};
    nate = {id: 2, name: 'Nate', email: '', school: mockSchoolID};
    mockDelegates = [jake, nate];

    ServerAPI.getDelegates.mockReturnValue(Promise.resolve(mockDelegates));
    ServerAPI.updateDelegate.mockReturnValue(Promise.resolve({}));
    ServerAPI.deleteDelegate.mockReturnValue(Promise.resolve({}));
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the delegates on first call and caches locally', () => {
    var delegates = DelegateStore.getDelegates(mockSchoolID);
    expect(delegates.length).toEqual(0);
    expect(ServerAPI.getDelegates).toBeCalledWith(mockSchoolID);

    registerCallback({
      actionType: ActionConstants.DELEGATES_FETCHED,
      schoolID: mockSchoolID,
      delegates: mockDelegates
    });

    delegates = DelegateStore.getDelegates(mockSchoolID);
    expect(delegates).toEqual(mockDelegates);
    expect(ServerAPI.getDelegates.mock.calls.length).toEqual(1);
  });

  it('emits a change when the delegates are loaded', function() {
    var callback = jest.genMockFunction();
    DelegateStore.addListener(callback);
    expect(callback).not.toBeCalled();
    registerCallback({
      actionType: ActionConstants.DELEGATES_FETCHED,
      schoolID: mockSchoolID,
      delegates: mockDelegates
    });
    expect(callback).toBeCalled();
  });

  it('adds a delegate and emits a change', () => {
    registerCallback({
      actionType: ActionConstants.DELEGATES_FETCHED,
      schoolID: mockSchoolID,
      delegates: mockDelegates
    });

    var callback = jest.genMockFunction();
    DelegateStore.addListener(callback);
    expect(callback).not.toBeCalled();

    var new_delegate = {id: 3, name: 'Trevor', email: "", school: mockSchoolID};
    registerCallback({
      actionType: ActionConstants.ADD_DELEGATE,
      delegate: new_delegate
    });
    expect(callback).toBeCalled();

    var delegates = DelegateStore.getDelegates(mockSchoolID);
    expect(delegates.length).toEqual(3);
    expect(new_delegate).toEqual(delegates[2]);
  });

  it('deletes a delegate and emits a change', () => {
    registerCallback({
      actionType: ActionConstants.DELEGATES_FETCHED,
      schoolID: mockSchoolID,
      delegates: mockDelegates
    });

    var callback = jest.genMockFunction();
    DelegateStore.addListener(callback);
    expect(callback).not.toBeCalled();

    registerCallback({
      actionType: ActionConstants.DELETE_DELEGATE,
      delegateID: 1
    });
    expect(callback).toBeCalled();
    expect(ServerAPI.deleteDelegate).toBeCalledWith(1);

    var delegates = DelegateStore.getDelegates(mockSchoolID);
    expect(delegates.length).toEqual(1);
    expect(delegates[0]).toEqual(nate);
  });

  it('updates a delegate and emits a change', () => {
    registerCallback({
      actionType: ActionConstants.DELEGATES_FETCHED,
      schoolID: mockSchoolID,
      delegates: mockDelegates
    });

    var callback = jest.genMockFunction();
    DelegateStore.addListener(callback);
    expect(callback).not.toBeCalled();

    var delta = {name: 'Jake Moskowitz', email: 'j@m.com'};
    registerCallback({
      actionType: ActionConstants.UPDATE_DELEGATE,
      delegateID: 1,
      delta: delta
    });
    expect(callback).toBeCalled();

    var updated_jake = DelegateStore.getDelegates(mockSchoolID)[0];
    expect(ServerAPI.updateDelegate).toBeCalledWith(1, updated_jake);
    expect(updated_jake.name).toEqual(delta.name);
    expect(updated_jake.email).toEqual(delta.email);
  });

  it('updates delegates in bulk and emits a change', () => {
    registerCallback({
      actionType: ActionConstants.DELEGATES_FETCHED,
      schoolID: mockSchoolID,
      delegates: mockDelegates
    });

    var callback = jest.genMockFunction();
    DelegateStore.addListener(callback);
    expect(callback).not.toBeCalled();

    var updated_jake = {id: 1, name: 'Jake Moskowitz', email: '', school: mockSchoolID};
    var udpated_nate = {id: 2, name: 'Nathaniel Parke', email: '', school: mockSchoolID};
    registerCallback({
      actionType: ActionConstants.UPDATE_DELEGATES,
      schoolID: mockSchoolID,
      delegates: [updated_jake, udpated_nate]
    });
    expect(callback).toBeCalled();
    expect(ServerAPI.updateSchoolDelegates).toBeCalledWith(
      mockSchoolID,
      [updated_jake, udpated_nate]
    );

    var updated_delegates = DelegateStore.getDelegates(mockSchoolID);
    expect(updated_delegates.length).toEqual(2);
    expect(updated_jake).toEqual(updated_delegates[0]);
    expect(udpated_nate).toEqual(updated_delegates[1]);
  });
});
