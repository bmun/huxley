/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

"use strict";

import React from "react";
import PropTypes from "prop-types";

var {ConferenceContext} = require("components/ConferenceContext");
var {NavLink} = require("components/NavLink");
var {OuterView} = require("components/OuterView");
var {TextTemplate} = require("components/core/TextTemplate");

require("css/Letter.less");
var RegistrationClosedViewText = require("text/RegistrationClosedViewText.md");

class RegistrationClosedView extends React.Component {
  render() {
    return (
      <OuterView>
        <div className="letter">
          <TextTemplate conferenceSession={global.conference.session}>
            {RegistrationClosedViewText}
          </TextTemplate>
        </div>
        <hr />
        <NavLink direction="right" href="/login">
          Proceed to Login
        </NavLink>
      </OuterView>
    );
  }
}

export {RegistrationClosedView};
