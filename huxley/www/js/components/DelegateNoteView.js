/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

'use strict';

import React from "react";
import { history } from "utils/history";

const { AssignmentStore } = require('stores/AssignmentStore');
const { Button } = require('components/core/Button');
const { CurrentUserStore } = require('stores/CurrentUserStore');
const { InnerView } = require('components/InnerView');
const { TextTemplate } = require('components/core/TextTemplate');
const { User } = require('utils/User');
const { NoteConversation } = require('components/notes/NoteConversation');
const { NoteConversationSelector } = require('components/notes/NoteConversationSelector');
const { NoteStore } = require('stores/NoteStore');


const { ServerAPI } = require('lib/ServerAPI');

class DelegateNoteView extends React.Component {
  constructor(props) {
    super(props);
    const user = CurrentUserStore.getCurrentUser();
    const user_assignment = user.delegate.assignment;
    const conversation = NoteStore.getConversationNotes(user_assignment.id, null, true);
    console.log(user_assignment.committee);
    const assignments = AssignmentStore.getCommitteeAssignments(user_assignment.committee.id);

    // var assignments = AssignmentStore.getCommitteeAssignments(user.committee);
    // var countries = CountryStore.getCountries();
    // var delegates = DelegateStore.getCommitteeDelegates(user.committee);
    // var attendance = this._mapAttendance(delegates);
    // if (assignments.length && Object.keys(countries).length) {
    //   assignments.sort((a1, a2) =>
    //     countries[a1.country].name < countries[a2.country].name ? -1 : 1
    //   );
    // }

    this.state = {
      conversation: conversation,
      sender: user_assignment,
      assignments: assignments
    };
  }


  UNSAFE_componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isDelegate(user)) {
      history.redirect("/");
    }
  }

  componentDidMount() {
    this._conversationToken = NoteStore.addListener(() => {
      console.log('test1')
      this.setState({
        conversation: NoteStore.getConversationNotes(this.state.sender.id, null, true),
      });
    });

    this._assignmentToken = AssignmentStore.addListener(() => {
      console.log('test');
      this.setState({
        assignments: AssignmentStore.getCommitteeAssignments(this.state.sender.committee.id),
      });
    });
  }

  componentWillUnmount() {
    this._conversationToken && this._conversationToken.remove();
    this._assignmentToken && this._assignmentToken.remove();
  }

  render() {
    return (
      <InnerView>
        <table width={'100%'}>
          <tbody>
            <tr>
              <td width={'20%'}>
                <NoteConversationSelector assignments={this.state.assignments} onChairConversationChange={this._onChairConversationChange}
                            onConversationChange = {this._onConversationChange}/>
              </td>
              <td width={'80%'}>
                <NoteConversation sender_id={this.state.sender.id} is_chair='2' conversation={this.state.conversation} />
              </td>
            </tr>
          </tbody>
        </table>
      </InnerView>)
  }

  _onChairConversationChange: () => void = () => {
    console.log('hi!!!');
  }

  _onConversationChange: (any) => void = (assignment) => {
    console.log('hi - for for a delegate!!!');
    console.log(assignment);
  }
};

export { DelegateNoteView };
