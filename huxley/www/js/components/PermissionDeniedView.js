/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var React = require('react');

var TextTemplate = require('components/TextTemplate');

var PermissionDeniedViewText = require('text/PermissionDeniedViewText.md');

var PermissionDeniedView = React.createClass({
  render: function() {
    return (
      <div>
        <TextTemplate>
          {PermissionDeniedViewText}
        </TextTemplate>
      </div>
    );
  }
});

module.exports = PermissionDeniedView;
