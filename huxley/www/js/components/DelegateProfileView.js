/**
 * Copyright (c) 2011-2016 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

"use strict";

import React from "react";
import PropTypes from "prop-types";
import { history } from "utils/history";

const { Button } = require("components/core/Button");
const { ConferenceContext } = require("components/ConferenceContext");
const { CurrentUserStore } = require("stores/CurrentUserStore");
const { InnerView } = require("components/InnerView");
const { TextTemplate } = require("components/core/TextTemplate");
const { User } = require("utils/User");

require("css/Table.less");
const DelegateProfileViewText = require("text/DelegateProfileViewText.md");

const DelegateChecklistPositionPaperText = require("text/checklists/DelegateChecklistPositionPaperText.md");
const DelegateChecklistWaiverText = require("text/checklists/DelegateChecklistWaiverText.md");
const DelegateProfileNoZoomViewText = require("text/DelegateProfileNoZoomViewText.md");
// const DelegateProfileZoomViewText = require("text/DelegateProfileZoomViewText.md");

class DelegateProfileView extends React.Component {
  constructor(props) {
    super(props);
    var user = CurrentUserStore.getCurrentUser();
    var delegate = user.delegate;
    this.state = {
      delegate: delegate,
    };
  }

  UNSAFE_componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isDelegate(user)) {
      history.redirect("/");
    }
  }

  render() {
    var user = CurrentUserStore.getCurrentUser();
    var delegate = this.state.delegate;
    var assignment = delegate && delegate.assignment;
    var committee = delegate && delegate.assignment.committee;
    var country = delegate && delegate.assignment.country;
    var school = delegate && delegate.school;
    var summary = <div />;
    var text = <div />;
    var zoomLinkText = <div />;

    if (assignment && school && committee && country) {
      text = (
        <TextTemplate
          firstName={delegate.name}
          schoolName={school.name}
          conferenceSession={global.conference.session}
          committee={committee.full_name}
          country={country.name}
        >
          {DelegateProfileViewText}
        </TextTemplate>
      );
    }

    var positionPaperCheck = "";
    if (assignment && assignment.paper && assignment.paper.file) {
      positionPaperCheck = "\u2611";
    } else {
      positionPaperCheck = "\u2610";
    }

    var waiverCheck = "";
    if (delegate && delegate.waiver_submitted) {
      waiverCheck = "\u2611";
    } else {
      waiverCheck = "\u2610";
    }

    var checklist = (
      <table>
        <thead>
          <tr>
            <th>Delegate Checklist</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              {positionPaperCheck} <b>Turn in Position Paper</b>
              <br />
              <TextTemplate
                earlyPaperDeadlineMonth={
                  global.conference.early_paper_deadline["month"]
                }
                earlyPaperDeadlineDay={
                  global.conference.early_paper_deadline["day"]
                }
                paperDeadlineMonth={global.conference.paper_deadline["month"]}
                paperDeadlineDay={global.conference.paper_deadline["day"]}
              >
                {DelegateChecklistPositionPaperText}
              </TextTemplate>
            </td>
          </tr>
          <tr>
            <td>
              {waiverCheck} <b>Turn in Waiver Form</b>
              <br />
              <TextTemplate
                conferenceExternal={global.conference.external}
                waiverAvail={global.conference.waiver_avail_date}
                waiverDeadline={global.conference.waiver_deadline}
                waiverLink={global.conference.waiver_link}
              >
                {DelegateChecklistWaiverText}
              </TextTemplate>
            </td>
          </tr>
        </tbody>
      </table>
    );

    // if (committee) { 
    //   if (delegate && delegate.waiver_submitted) {
    //     zoomLinkText = (
    //               <div>
    //                 <th>Committee Zoom Link</th>
    //                 <br />
    //                 <Button
    //                   color="blue"
    //                   size="small"
    //                   onClick={() => window.open(committee.zoom_link, "_blank")}
    //                 >
    //                   Click here to join committee!
    //                 </Button>
    //               </div>
    //               );
    //   } else {
    //     zoomLinkText = (
    //               <div>
    //                 <th>Committee Zoom Link</th>
    //                 <b />
    //                 <TextTemplate
    //                   opiLink = {global.conference.opi_link}
    //                 >
    //                   {DelegateProfileNoZoomViewText}
    //                 </TextTemplate>
    //               </div>
    //               );
    //   }    
    // }

    if (delegate.published_summary) {
      summary = (
        <table>
          <thead>
            <tr>
              <th>Feedback From Your Chairs:</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{delegate.published_summary}</td>
            </tr>
          </tbody>
        </table>
      );
    }

    return (
      <InnerView>
        <div style={{ textAlign: "center" }}>
          <br />
          <h2>We are excited to have you at BMUN this year!</h2>
          <br />
        </div>
        {text}
        <br />
        {checklist}
        {zoomLinkText}
        {summary}
      </InnerView>
    );
  }
}

export { DelegateProfileView };
