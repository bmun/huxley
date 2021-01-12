/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";


require("css/Table.less");

class Table extends React.Component {
  render() {
    const { emptyMessage, isEmpty, children } = this.props;
    return (
      <div className="table-container">
        <table>{this.props.children}</table>
        {isEmpty ? <div className="empty help-text">{emptyMessage}</div> : null}
      </div>
    );
  }
}

Table.propTypes = {
  emptyMessage: PropTypes.string.isRequired,
  isEmpty: PropTypes.bool.isRequired,
};


