/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var HtmlToReactParser = require('html-to-react').Parser;

/**
 * A general purpose function to replace words in a string
 * with a given dictionary of words
 */
function _transformMarkdownToReact(text, variables) {
    for (const variable of Object.keys(variables)) {
    	var regex = new RegExp("{{ " + variable + " }}", "g");
    	text = text.replace(regex, variables[variable]);
    }

    var htmlToReactParser = new HtmlToReactParser();
    var reactElement = htmlToReactParser.parse(text);

    return reactElement;
}

module.exports = _transformMarkdownToReact;
