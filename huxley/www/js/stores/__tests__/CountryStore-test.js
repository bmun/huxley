/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/CountryStore');

describe('CountryStore', () => {
  var ActionConstants;
  var CountryStore;
  var Dispatcher;
  var ServerAPI;

  var mockCountries;
  var registerCallback;

  beforeEach(() => {
    ActionConstants = require('constants/ActionConstants');
    CountryStore = require('stores/CountryStore');
    Dispatcher = require('dispatcher/Dispatcher');
    ServerAPI = require('lib/ServerAPI');

    registerCallback = function(action) {
      Dispatcher.isDispatching.mockReturnValue(true);
      Dispatcher.register.mock.calls[0][0](action);
      Dispatcher.isDispatching.mockReturnValue(false);
    };

    mockCountries = [{id: 1, name: 'USA'}, {id: 2, name: 'China'}];
    ServerAPI.getCountries.mockReturnValue(Promise.resolve(mockCountries));
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the countries on first call and caches locally', () => {
    var countries = CountryStore.getCountries();
    expect(countries).toEqual({});
    expect(ServerAPI.getCountries).toBeCalled();

    registerCallback({
      actionType: ActionConstants.COUNTRIES_FETCHED,
      countries: mockCountries,
    });

    countries = CountryStore.getCountries();
    expect(Object.values(countries)).toEqual(mockCountries);
    expect(ServerAPI.getCountries.mock.calls.length).toEqual(1);
  });

  it('emits a change when the countries are loaded', function() {
    var callback = jest.genMockFunction();
    CountryStore.addListener(callback);
    expect(callback).not.toBeCalled();
    registerCallback({
      actionType: ActionConstants.COUNTRIES_FETCHED,
      countries: mockCountries,
    });
    expect(callback).toBeCalled();
  });
});
