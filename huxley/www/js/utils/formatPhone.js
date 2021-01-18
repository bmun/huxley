/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

/**
 * Given an input string, output a string in the format (NNN) NNN-NNNN xNNNNN.
 *
 * This is done by using a finite-state-machine, where each state is a
 * particular index (or "slot") of the final target string.

 * At each slot, apply a transition function that peeks at the next token of
 * the input, possibly consumes it, and returns whether to transition to the
 * next slot.
 *
 * The process ends when we reach the last slot or run out of input tokens.
 */
function formatPhone(rawInput) {
  var input = _tokenize(rawInput);
  var accumulator = [];

  for (var slot = 0; slot <= 20 && input.length > 0; ) {
    var f = _getTransitionFunction(slot);
    var shouldTransition = f(accumulator, input);
    shouldTransition && ++slot;
  }

  return accumulator.join("");
}

/**
 * Get the transition function for a particular slot.
 *
 * A transition function:
 *  - accepts the accumulator and the input,
 *  - adds to the accumulator based on the next token of the input, and
 *  - returns whether to transition to the next slot.
 *
 * See the docblocks of the transition functions below for more details.
 */
function _getTransitionFunction(slot) {
  switch (slot) {
    case 0:
      return _leftParen;
    case 1:
    case 2:
    case 3:
      return _digit;
    case 4:
      return _rightParen;
    case 5:
      return _space;
    case 6:
    case 7:
    case 8:
      return _digit;
    case 9:
      return _dash;
    case 10:
    case 11:
    case 12:
    case 13:
      return _digit;
    case 14:
      return _space;
    case 15:
      return _x;
    default:
      return _digit;
  }
}

/**
 * Always push a the given token type onto the output.
 * Consume the next token only if it's the given token type.
 * Always transition.
 */
function _singleToken(token) {
  return function (accumulator, input) {
    if (input[0] === token) {
      input.shift();
    }
    accumulator.push(token);
    return true;
  };
}

var _leftParen = _singleToken("(");
var _rightParen = _singleToken(")");
var _dash = _singleToken("-");
var _space = _singleToken(" ");
var _x = _singleToken("x");

/**
 * Push the next token onto the output only if it's a digit.
 * Always consume the next token.
 * Transition only if the next token is a digit.
 */
function _digit(accumulator, input) {
  var token = input.shift();
  if (!token.match(/\d/)) {
    return false;
  }

  accumulator.push(token);
  return true;
}

/**
 * Remove invalid characters, strip leading whitespace/dashes/right-parens/x,
 * and split into an array.
 */
function _tokenize(input) {
  return input
    .replace(/[^\d\s\(\)\-x]+/, "")
    .replace(/^[\s\-\)x]+/, "")
    .split("");
}

export { formatPhone };
