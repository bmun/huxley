/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

import ActionConstants from 'constants/ActionConstants';
import {CountryActions} from 'actions/CountryActions';
import {Dispatcher} from 'dispatcher/Dispatcher';
import {ServerAPI} from 'lib/ServerAPI';
import {Store} from'flux/utils';

var _countries = {};

class CountryStore extends Store {
  getCountries() {
    if (Object.keys(_countries).length) {
      return _countries;
    }

    ServerAPI.getCountries().then(value => {
      CountryActions.countriesFetched(value);
    });

    return {};
  }

  __onDispatch(action) {
    switch (action.actionType) {
      case ActionConstants.COUNTRIES_FETCHED:
        for (const country of action.countries) {
          _countries[country.id] = country;
        }
        break;
      default:
        return;
    }

    this.__emitChange();
  }
}

const countryStore = new CountryStore(Dispatcher);
export {countryStore as CountryStore};
