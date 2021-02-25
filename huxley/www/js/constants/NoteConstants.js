/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */
//@flow

"use strict";
const blacklistedWords = require('utils/_blacklistedWords.json');

const PollingInterval = 4000;
const webTerms = [`https`, "http", `\\.com`, `\\.org`, `\\.net`, `\\.edu`, `www`];
const blacklistedWordsRegexp: Array<RegExp> = blacklistedWords["words"].map(
    word => RegExp(
        `([\\(\\)\\.\\-?!;:,\\s\u2026"]|^)${word.toLowerCase()}([\\(\\)\\.\\-?!;:,\\s\u2026"]|$)`
      )
);
const webTermsRegexp = webTerms.map(word => RegExp(word));
const SearchTerms: Array<RegExp> = webTermsRegexp.concat(blacklistedWordsRegexp);

export { PollingInterval, SearchTerms};
