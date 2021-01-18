/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import ActionConstants from "constants/ActionConstants";
import { Dispatcher } from "dispatcher/Dispatcher";

var SecretariatMemberActions = {
  secretariatMembersFetched(secretariatMembers) {
    Dispatcher.dispatch({
      actionType: ActionConstants.SECRETARIAT_MEMBERS_FETCHED,
      secretariatMembers: secretariatMembers,
    });
  },
};

export { SecretariatMemberActions };
