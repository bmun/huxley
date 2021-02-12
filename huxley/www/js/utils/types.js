/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */
/* Model types for flow. Currently in the process of migration. */
//@flow

type Assignment = { id: number, country: number, ... };

type CommitteeFeedback = { ... };

type Committee = { ... };

type Country = { ... };

type Delegate = { ... };

type Note = {
  id?: number,
  sender: ?number,
  recipient: ?number,
  is_chair: number,
  msg: string,
  timestamp?: number,
};

type PositionPaper = { ... };

type Registration = { ... };

type Rubric = { ... };

type SecretariatMember = { ... };

export type {
  Assignment,
  CommitteeFeedback,
  Committee,
  Country,
  Delegate,
  Note,
  PositionPaper,
  Registration,
  Rubric,
  SecretariatMember,
};
