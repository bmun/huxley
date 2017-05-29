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
      var value  = this.escapeHtml(this.props[variable]);
      markdown = markdown.replace(regex, value);
    }

    return {__html: markdown};
  },

  escapeHtml: function(string) {
    var entityMap = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
      '/': '&#x2F;',
      '`': '&#x60;',
      '=': '&#x3D;'
    };

    return String(string).replace(/[&<>"'`=\/]/g, function (s) {
      return entityMap[s];
    });
  }
});

module.exports = MarkdownTemplate;
