/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */
/* Model types for flow. Currently in the process of migration. */
//@flow

type Assignment = {
  id: number,
  committee: number,
  country: number,
  paper: PositionPaper,
  registration: number,
  rejected: boolean,
};

type AssignmentNested = {
  id: number,
  committee: Committee,
  country: Country,
  paper: PositionPaper,
  registration: number,
  rejected: boolean,
};

type CommitteeFeedback = { id: number, ... };

type Committee = {
  id: number,
  delegation_size: number,
  full_name: string,
  name: string,
  rubric: Rubric,
  special: boolean,
};

type Country = {
  id: number,
  name: string,
  special: boolean,
};

type Delegate = {
  id: number,
  assignment: AssignmentNested,
  committee_feedback_submitted: boolean,
  created_at: string,
  email: string,
  name: string,
  published_summary: string,
  school: School,
  session_four: boolean,
  session_one: boolean,
  session_three: boolean,
  session_two: boolean,
  summary: string,
  voting: boolean,
  waiver_submitted: boolean,
};

type Note = {
  id: number,
  sender: ?number,
  recipient: ?number,
  is_chair: number,
  msg: string,
  timestamp: number,
};

type PositionPaper = {
  id: number,
  file: ?string,
  graded: boolean,
  graded_file: ?string,
  score_1: number,
  score_2: number,
  score_3: number,
  score_4: number,
  score_5: number,
  score_t2_1: number,
  score_t2_2: number,
  score_t2_3: number,
  score_t2_4: number,
  score_t2_5: number,
  submission_date: ?string,
};

type Registration = { id: number, ... };

type Rubric = {
  id: number,
  grade_category_1: string,
  grade_category_2: string,
  grade_category_3: string,
  grade_category_4: string,
  grade_category_5: string,
  grade_t2_category_1: string,
  grade_t2_category_2: string,
  grade_t2_category_3: string,
  grade_t2_category_4: string,
  grade_t2_category_5: string,
  grade_t2_value_1: number,
  grade_t2_value_2: number,
  grade_t2_value_3: number,
  grade_t2_value_4: number,
  grade_t2_value_5: number,
  grade_value_1: number,
  grade_value_2: number,
  grade_value_3: number,
  grade_value_4: number,
  grade_value_5: number,
  topic_one: string,
  topic_two: string,
  use_topic_2: boolean,
};

type SecretariatMember = {
  id: number,
  committee: number,
  is_head_chair: boolean,
  name: string,
};

type School = {
  id: number,
  address: string,
  city: string,
  country: string,
  international: boolean,
  name: string,
  primary_email: string,
  primary_gender: number,
  primary_name: string,
  primary_phone: string,
  primary_type: number,
  program_type: number,
  secondary_email: string,
  secondary_gender: number,
  secondary_name: string,
  secondary_phone: string,
  secondary_type: number,
  state: string,
  times_attended: number,
  zip_code: string,
};

export type {
  Assignment,
  AssignmentNested,
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
