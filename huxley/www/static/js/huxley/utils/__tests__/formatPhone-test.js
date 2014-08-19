/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

jest.dontMock('../formatPhone');

describe('formatPhone', function() {
  it('should format phone numbers correctly in progress', function() {
    var formatPhone = require('../formatPhone');
    var testCases = [
      [' ', ''],
      ['hi', ''],
      ['(', '('],
      ['1', '(1'],
      [' 1', '(1'],
      ['1234', '(123) 4'],
      ['(123 ', '(123) '],
      ['(123) 456-', '(123) 456-'],
      ['(123) 456 7', '(123) 456-7'],
      ['(123) 45678', '(123) 456-78'],
      ['1234567890', '(123) 456-7890'],
      ['(12) 345-6789', '(123) 456-789'],
      ['(1234)5678', '(123) 456-78'],
      ['(123) 456-7890 1', '(123) 456-7890 x1'],
      ['(123) 456-78901111', '(123) 456-7890 x1111'],
      ['(123) 456-7890 x1234567', '(123) 456-7890 x12345']
    ];

    testCases.forEach(function(testCase) {
      var input = testCase[0];
      var output = testCase[1];
      expect(formatPhone(input)).toEqual(output);
    });
  });
});
