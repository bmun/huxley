/**
* Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

"use strict";

import React from "react";

const { Button } = require("components/core/Button");
var { CommitteeStore } = require("stores/CommitteeStore");
var { InnerView } = require("components/InnerView");
var { TextTemplate } = require("components/core/TextTemplate");

require("css/Table.less");
var AdvisorZoomLinkViewText = require("text/AdvisorZoomLinkViewText.md");

class AdvisorZoomLinkView extends React.Component {
  constructor(props) {
    super(props);
    var committees = Object.values(CommitteeStore.getCommittees());

    this.state = {
      committees: committees,
    };
  }

  componentDidMount() {
    this._committeesToken = CommitteeStore.addListener(() => {
      var committees = Object.values(CommitteeStore.getCommittees());
      this.setState({ committees : committees });
    });

  }

  componentWillUnmount() {
    this._committeesToken && this._committeesToken.remove();
  }

  render() {
    return (
      <InnerView>
        <TextTemplate opiLink = {global.conference.opi_link}>{AdvisorZoomLinkViewText}</TextTemplate>
        <form>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Committee</th>
                  <th style={{textAlign:"right"}}>Zoom Link</th>
                </tr>
              </thead>
            </table>
            <div>
              <table className="table highlight-cells">
                <tbody>
                  {Object.keys(this.state.committees).length > 0 ? (
                    this.renderCommitteeRows()
                  ) : (
                    <tr />
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </form>
      </InnerView>
    );
  }

  renderCommitteeRows = () => {
    var committees = this.state.committees;
    return committees.map((committee) => {
      return (
        <tr key={committee.id}>
          <td>{committee.full_name} ({committee.name})</td>
          <td style={{textAlign:"right"}}>
          <Button
            color="blue"
            size="small"
            onClick={() => window.open(committee.zoom_link, "_blank")}
          >
            Join Call
          </Button>
          </td>
        </tr>
      );
    });
  };
}

export { AdvisorZoomLinkView };
