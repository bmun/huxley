/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

import {BrowserHistory} from 'utils/BrowserHistory';

const history = {
    redirect: (url) => {
        BrowserHistory.push(url);
        location.reload();
    }
}
export {history};
