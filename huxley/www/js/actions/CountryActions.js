/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import ActionConstants from "constants/ActionConstants";
import { Dispatcher } from "dispatcher/Dispatcher";

var CountryActions = {
  countriesFetched(countries) {
    Dispatcher.dispatch({
      actionType: ActionConstants.COUNTRIES_FETCHED,
      countries: countries,
    });
  },
};

export { CountryActions };
