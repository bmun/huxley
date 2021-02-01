/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

 //@flow

 type Note = {
    sender_id: ?number, 
    recipient_id: ?number, 
    is_chair: number, 
    msg: string, 
    timestamp?: number
 }

 export type {Note}