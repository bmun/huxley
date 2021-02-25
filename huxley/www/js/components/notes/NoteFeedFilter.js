/**
 * Copyright (c) 2011-2021 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 +*/

//@flow

"use strict";

import React from "react";
import type { Assignment } from "utils/types";

const { Button } = require("components/core/Button");

// $FlowFixMe
require("css/notes/NoteFeedFilter.less");
type NoteFeedFilterProps = {
  assignments: { [string]: Assignment },
  onInputChange: (string, ?Assignment, ?Assignment, boolean) => void,
};

type NoteFeedFilterState = {
  query: string,
  sender: string,
  recipient: string,
  flagged: boolean,
};

class NoteFeedFilter extends React.Component<
  NoteFeedFilterProps,
  NoteFeedFilterState
> {
  constructor(props: NoteFeedFilterProps) {
    super(props);
    this.state = {
      query: "",
      sender: "",
      recipient: "",
      flagged: false,
    };
  }

  render(): React$Element<any> {
    return (
      <div className="feedFilter">
        <form onSubmit={this._handleSubmit}>
          <datalist id="delegations">
            {Object.keys(this.props.assignments).map((country) => (
              <option key={country}>{country}</option>
            ))}
          </datalist>
          <div className="filter">
            <div>Keyword</div>
            <input
              className="filterInput"
              name="query"
              value={this.state.query}
              onChange={this._handleQueryChange}
            />
          </div>
          <div className="filter">
            <div>Sender</div>
            <input
              className="filterInput"
              name="sender"
              value={this.state.sender}
              list="delegations"
              onChange={this._handleSenderChange}
            />
          </div>
          <div className="filter">
            <div>Recipient</div>
            <input
              className="filterInput"
              name="recipient"
              value={this.state.recipient}
              list="delegations"
              onChange={this._handleRecipientChange}
            />
          </div>
          <div className="filter">
            <div>Flagged</div>
            <input
              className="flaggedCheckbox"
              name="flagged"
              type="checkbox"
              checked={this.state.flagged}
              onChange={this._handleFlaggedChange}
            />
          </div>
          <input type="submit" style={{ display: "none" }} />
        </form>
        <span className="rightButtons">
            <Button size="small" onClick={this._handleSubmit} color="blue">
            Filter
          </Button>
          <span className="clearFilter">
          <Button size="small" onClick={this._clearFilters} color="red">
            Clear Filters
          </Button>
          </span>
        </span>
      </div>
    );
  }

  _clearFilters: () => void = () => {
    this.setState({
      query: "",
      sender: "",
      recipient: "",
      flagged: false,
    });
    this.props.onInputChange("", null, null, false);
  };

  _handleFlaggedChange: (SyntheticEvent<HTMLInputElement>) => void = (
    event
  ) => {
    if (
      event.target instanceof HTMLInputElement &&
      event.target.type === "checkbox"
    ) {
      this.setState({ flagged: event.target.checked });
    }
  };

  _handleQueryChange: (SyntheticEvent<HTMLInputElement>) => void = (event) => {
    if (event.target instanceof HTMLInputElement) {
      this.setState({ query: event.target.value });
    }
  };

  _handleSenderChange: (SyntheticEvent<HTMLInputElement>) => void = (event) => {
    if (event.target instanceof HTMLInputElement) {
      this.setState({ sender: event.target.value });
    }
  };

  _handleRecipientChange: (SyntheticEvent<HTMLInputElement>) => void = (
    event
  ) => {
    if (event.target instanceof HTMLInputElement) {
      this.setState({ recipient: event.target.value });
    }
  };

  _handleSubmit: (SyntheticEvent<HTMLInputElement>) => void = (event) => {
    this.props.onInputChange(
      this.state.query,
      this.props.assignments[this.state.sender],
      this.props.assignments[this.state.recipient],
      this.state.flagged
    );
    event.preventDefault();
  };
}

export { NoteFeedFilter };
