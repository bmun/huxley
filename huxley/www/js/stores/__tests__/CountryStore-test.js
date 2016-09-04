/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/CountryStore');

describe('CountryStore', () => {
  var CountryStore;
  var Dispatcher;
  var ServerAPI;

  var mockCountries;

  beforeEach(() => {
    CountryStore = require('stores/CountryStore');
    Dispatcher = require('dispatcher/Dispatcher');
    ServerAPI = require('lib/ServerAPI');

    mockCountries = [{id: 1, name: 'USA'}, {id: 2, name: 'China'}];
    ServerAPI.getCountries.mockReturnValue(Promise.resolve(mockCountries));
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the countries on first call and caches locally', () => {
    return Promise.all([
      CountryStore.getCountries().then((countries) => {
        expect(countries).toEqual(mockCountries);
      }),
      CountryStore.getCountries().then((countries) => {
        expect(countries).toEqual(mockCountries);
      }),
    ]);
  });
});
