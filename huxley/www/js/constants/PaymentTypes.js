/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

 "use strict";

 import invariant from "invariant";
 
 invariant(
   global.PaymentTypes !== undefined,
   "global.PaymentTypes must be defined."
 );
 
 var PaymentTypes = global.PaymentTypes;
 delete global.PaymentTypes;
 
 export { PaymentTypes };
 