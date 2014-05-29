/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
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

    mockCountries = [{id: 1, name: 'USA'}, {id: 2, name: 'China'}];
    $.ajax.mockReturnValue({
      done: function(callback) {
        callback(null, null, {responseJSON: mockCountries});
      }
    });
  });

  it('requests the countries on first call and caches locally', function() {
    CountryStore.getCountries(function(countries) {
      expect($.ajax).toBeCalledWith({
        type: 'GET',
        url: '/api/countries',
        dataType: 'json'
      });
      expect(countries).toEqual(mockCountries);
    });
    CountryStore.getCountries(function(countries) {
      expect($.ajax.mock.calls.length).toBe(1);
      expect(countries).toEqual(mockCountries);
    });
  });
});
