/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

 'use strict';

 var React = require('react');
 var ReactRouter = require('react-router');
 
 var Button = require('components/core/Button');
 var ConferenceContext = require('components/ConferenceContext');
 var CurrentUserStore = require('stores/CurrentUserStore');
 var InnerView = require('components/InnerView');
 var TextTemplate = require('components/core/TextTemplate');
 var User = require('utils/User');
 var NoteMessageBox = require('components/NoteMessageBox')
 
 
 var ServerAPI = require('lib/ServerAPI');
  
 var DelegateNoteView = React.createClass({
   mixins: [ReactRouter.History],
 
   contextTypes: {
     conference: React.PropTypes.shape(ConferenceContext),
   },
 
//    getInitialState() {
     
//    },
 
   componentWillMount() {
     var user = CurrentUserStore.getCurrentUser();
     if (!User.isDelegate(user)) {
       this.history.pushState(null, '/');
     }
   },
 
//    componentDidMount() {
     
//    },
 
//    componentWillUnmount() {
//    },
 
   render() {
     return <InnerView> <NoteMessageBox/> </InnerView>;
   },
 
   
 });
 
 module.exports = DelegateNoteView;
 