/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

/**
 * A general purpose function to handle onChange events
 * Handles changes from both HTML and custom components
 */
function _handleChange(fieldName, event) {
  this.setState({
    [fieldName]: event.target ? event.target.value : event,
  });
}

export {_handleChange};
