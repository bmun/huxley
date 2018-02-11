/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var Button = require('components/core/Button');
var CurrentUserStore = require('stores/CurrentUserStore');
var InnerView = require('components/InnerView');
var PaperSubmissionTable = require('components/PaperSubmissionTable');
var PositionPaperActions = require('actions/PositionPaperActions');
var PositionPaperStore = require('stores/PositionPaperStore');
var TextTemplate = require('components/core/TextTemplate');
var User = require('utils/User');

var ServerAPI = require('lib/ServerAPI');

require('css/Table.less');
var DelegatePaperViewText = require('text/DelegatePaperViewText.md');

var DelegatePaperView = React.createClass({
  mixins: [ReactRouter.History],

  getInitialState() {
    var user = CurrentUserStore.getCurrentUser();
    PositionPaperActions.storePositionPaper(user.delegate.assignment.paper);
    var papers = PositionPaperStore.getPapers();
    var assignment = user.delegate.assignment;
    if (assignment.paper.file != null) {
      PositionPaperActions.fetchPositionPaperFile(assignment.paper.id);
    }
    var files = PositionPaperStore.getPositionPaperFiles();

    return {
      papers: papers,
      uploadedFile: null,
      files: files,
      errors: {},
    };
  },

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isDelegate(user)) {
      this.history.pushState(null, '/');
    }
  },

  componentDidMount() {
    this._papersToken = PositionPaperStore.addListener(() => {
      this.setState({
        files: PositionPaperStore.getPositionPaperFiles(),
        papers: PositionPaperStore.getPapers(),
      });
    });
  },

  componentWillUnmount() {
    this._papersToken && this._papersToken.remove();
    this._successTimeout && clearTimeout(this._successTimeout);
  },

  render() {
    return (
      <InnerView>
        <div style={{margin: 'auto 20px 20px 20px'}}>
          <TextTemplate>{DelegatePaperViewText}</TextTemplate>
        </div>
        <form>
          <div className="table-container">{this.renderRubric()}</div>
        </form>
      </InnerView>
    );
  },

  renderRubric() {
    const user = CurrentUserStore.getCurrentUser();
    const paper = this.state.papers[user.delegate.assignment.paper.id];
    const files = this.state.files;
    const rubric = user.delegate.assignment.committee.rubric;

    if (rubric != null && paper != null) {
      return (
        <PaperSubmissionTable
          rubric={rubric}
          paper={paper}
          files={files}
          onUpload={this._handleUploadPaper}
          onSubmit={this._handleSubmitPaper}
        />
      );
    } else {
      return <div />;
    }
  },

  _handleUploadPaper(paperID, event) {
    this.setState({uploadedFile: event.target.files[0]});
  },

  _handleSubmitPaper(paperID, event) {
    var file = this.state.uploadedFile;
    if (
      file != null &&
      window.confirm(
        `Please make sure this is the file you intend to submit! You have uploaded: ${
          file.name
        }.`,
      )
    ) {
      var paper = {...this.state.papers[paperID]};
      paper.file = file.name;

      PositionPaperActions.uploadPaper(
        paper,
        file,
        this._handleSuccess,
        this._handleError,
      );

      this.setState({
        uploadedFile: null,
      });
    }
    this.history.pushState(null, '/');
    event.preventDefault();
  },

  _handleSuccess: function(response) {
    window.alert('Your paper has been successfully uploaded!');
  },

  _handleError: function(response) {
    window.alert(
      'Something went wrong. Please refresh your page and try again.',
    );
  },
});

module.exports = DelegatePaperView;
