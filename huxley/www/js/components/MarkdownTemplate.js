/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var MarkdownTemplate = React.createClass({
  render: function() {
    return (
      <div dangerouslySetInnerHTML={this.createMarkup()} />
    );
  },

  createMarkup: function() {
    var markdown = this.props.children;
    for (const variable of Object.keys(this.props)) {
      var regex = new RegExp("{{ " + variable + " }}", "g");
      markdown = markdown.replace(regex, this.props[variable]);
    }

    return {__html: markdown};
  }
});

module.exports = MarkdownTemplate;
