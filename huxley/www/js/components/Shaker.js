/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import ReactDOM from "react-dom";
import cx from "classnames";

require("css/Shaker.less");

const ShakerContext = React.createContext(() => null);
class Shaker extends React.Component {
  render() {
    return (
      <ShakerContext.Provider value={this.shake}>
        <div className={cx("shaker", this.props.className)}>
          {this.props.children}
        </div>
      </ShakerContext.Provider>
    );
  }

  shake = () => {
    const element = ReactDOM.findDOMNode(this);
    if (element) {
      this._timeout && clearTimeout(this._timeout);
      element.classList.remove("shake");
      element.classList.add("shake");
      this._timeout = setTimeout(() => {
        element.classList.remove("shake");
      }, 301);
    }
  };
}

export { Shaker, ShakerContext };
