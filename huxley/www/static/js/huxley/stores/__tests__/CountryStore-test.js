/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('stores/CountryStore');

describe('CountryStore', () => {
  var $;
  var CountryStore;
  var Dispatcher;

  var mockCountries;

  beforeEach(() => {
    $ = require('jquery');
    CountryStore = require('stores/CountryStore');
    Dispatcher = require('dispatcher/Dispatcher');

    mockCountries = [{id: 1, name: 'USA'}, {id: 2, name: 'China'}];
    $.ajax.mockImplementation((options) => {
      options.success(null, null, {responseJSON: mockCountries});
    });
  });

  it('subscribes to the dispatcher', () => {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the countries on first call and caches locally', () => {
    return Promise.all([
      CountryStore.getCountries().then((countries) => {
        expect($.ajax).toBeCalledWith({
          type: 'GET',
          url: '/api/countries',
          dataType: 'json',
          success: jasmine.any(Function),
        });
        expect(countries).toEqual(mockCountries);
      }),
      CountryStore.getCountries().then((countries) => {
        expect($.ajax.mock.calls.length).toBe(1);
        expect(countries).toEqual(mockCountries);
      }),
    ]);
  });
});
