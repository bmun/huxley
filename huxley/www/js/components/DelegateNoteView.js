/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

 'use strict';

 import React from "react";
import { history } from "utils/history";
 
 var {Button} = require('components/core/Button');
 var {CurrentUserStore} = require('stores/CurrentUserStore');
 var {InnerView} = require('components/InnerView');
 var {TextTemplate} = require('components/core/TextTemplate');
 var {User} = require('utils/User');
 var {NoteMessageBox} = require('components/NoteMessageBox')
 const {NoteStore} = require('stores/NoteStore');
 
 
 var {ServerAPI} = require('lib/ServerAPI');
  
 class DelegateNoteView extends React.Component {
  constructor(props) {
    super(props);
    const user = CurrentUserStore.getCurrentUser();
    const user_assignment = user.delegate.assignment;
    const conversation = NoteStore.getConversationNotes(user_assignment.id, null, true);

    this.state = {
      conversation: conversation,
      assignment: user_assignment
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
      this.setState({
        conversation: NoteStore.getConversationNotes(this.state.assignment.id, null, true),
      });
    });
  }

  componentWillUnmount() {
    this._conversationToken && this._conversationToken.remove();
  }
 
//    componentDidMount() {
     
//    },
 
//    componentWillUnmount() {
//    },
 
   render() {
     return <InnerView> <NoteMessageBox conversation = {this.state.conversation} user_assignment = {this.state.assignment}/> </InnerView>;
   }
 
   
 };
 
 export { DelegateNoteView };
 