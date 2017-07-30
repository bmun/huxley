/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

const React = require('react');

const entityMap = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
  '/': '&#x2F;',
  '`': '&#x60;',
  '=': '&#x3D;',
};

const TextTemplate = React.createClass({
  render() {
    return <div dangerouslySetInnerHTML={this.createMarkup()} />;
  },

  createMarkup() {
    var text = this.props.children;
    for (const variable of Object.keys(this.props)) {
      const regex = new RegExp('{{ ' + variable + ' }}', 'g');
      const value = this.escapeHtml(this.props[variable]);
      text = text.replace(regex, value);
    }

    return {__html: text};
  },

  escapeHtml(string) {
    return String(string).replace(/[&<>"'`=\/]/g, function(s) {
      return entityMap[s];
    });
  },
});

module.exports = TextTemplate;
