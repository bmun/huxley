/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../CountryStore');

describe('CountryStore', function() {
  var $;
  var CountryStore;

  var mockCountries;

  beforeEach(function() {
    $ = require('jquery');
    CountryStore = require('../CountryStore');
    Dispatcher = require('../../dispatcher/Dispatcher');

    mockCountries = [{id: 1, name: 'USA'}, {id: 2, name: 'China'}];
    $.ajax.mockImplementation(function(options) {
      options.success(null, null, {responseJSON: mockCountries});
    });
  });

  it('subscribes to the dispatcher', function() {
    expect(Dispatcher.register).toBeCalled();
  });

  it('requests the countries on first call and caches locally', function() {
    var calls = 0;

    CountryStore.getCountries(function(countries) {
      calls++;
      expect($.ajax).toBeCalledWith({
        type: 'GET',
        url: '/api/countries',
        dataType: 'json',
        success: jasmine.any(Function),
      });
      expect(countries).toEqual(mockCountries);
    });
    jest.runAllTimers();

    CountryStore.getCountries(function(countries) {
      calls++;
      expect($.ajax.mock.calls.length).toBe(1);
      expect(countries).toEqual(mockCountries);
    });
    jest.runAllTimers();

    expect(calls).toBe(2);
  });
});
