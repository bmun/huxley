/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');

var InnerView = require('./InnerView');
var LogoutButton = require('./LogoutButton');
var User = require('../User');

var TYPE_CLUB = 1;
var TYPE_CLASS = 2;

var AdvisorProfileView = React.createClass({
  propTypes: {
    user: React.PropTypes.instanceOf(User).isRequired
  },

  render: function() {
    var user = this.props.user.getData();
    var school = user.school;
    return (
      <InnerView>
        <h2>Welcome, {user.first_name}!</h2>
        <p>We're very excited to see {school.name} at BMUN 63 this year! Here,
        you can view and edit your registration information for the conference,
        edit your delegate roster, and find answers to frequently asked
        questions. To edit your information, just click on any of the
        highlighted fields and add your changes. Also, <span className="bold">
        don't forget to save any information you update!</span></p>
        <br />
        <p><strong>Important Note:</strong> Please mail all checks to <strong>
        P.O. Box 4306 Berkeley, CA 94704-0306. If you have any other further
        questions contact me at <a href="mailto:info@bmun.org">
        info@bmun.org</a> and I will respond to all requests efficiently.
        See you soon!</strong></p>
        <br />
        <p className="bold">Who is the USG of External this year?
        <br />
        Under-Secretary General of External Relations, 63rd Session.</p>
        <form id="welcomepage">
          <div className="tablemenu header">
            Dont forget to save!
          </div>
          <div id="welcomeinfocontainer" className="table-container">
            <table id="welcomeinfo" className="table highlight-cells">
              <tr>
                <th colSpan="2">Advisor Information</th>
              </tr>
              <tr>
                <td className="fieldLabel">First Name</td>
                <td className="field">
                  <input
                    type="text"
                    value={user.first_name}
                  />
                </td>
              </tr>
              <tr>
                <td className="fieldLabel">Last Name</td>
                <td className="field">
                  <input
                    type="text"
                    value={user.last_name}
                  />
                </td>
              </tr>
              <tr>
                <th colSpan="2">School Information</th>
              </tr>
              <tr>
                <td className="fieldLabel">Name</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.name}
                  />
                </td>
              </tr>
              <tr>
                <td className="fieldLabel">Address</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.address}
                  />
                </td>
              </tr>
              <tr>
                <td className="fieldLabel">City</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.city}
                  />
                </td>
              </tr>
              <tr>
                <td className="fieldLabel">Zip</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.zip_code}
                  />
                </td>
              </tr>
              <tr>
                <th colSpan="2">Program Information</th>
              </tr>
              <tr>
                <td className="fieldLabel">Program Type</td>
                <td className="field">
                  <input
                    type="radio"
                    name="program_type"
                    value={TYPE_CLASS}
                    checked={TYPE_CLASS === school.program_type}
                  />
                  <label>Class</label>
                  &nbsp;&nbsp;&nbsp;&nbsp;
                  <input
                    type="radio"
                    name="program_type"
                    value={TYPE_CLUB}
                    checked={TYPE_CLUB === school.program_type}
                  />
                  <label>Club</label>
                </td>
              </tr>
              <tr>
                <td className="fieldLabel">Times Attended</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.times_attended}
                  />
                </td>
              </tr>
              <tr>
                <td className="fieldLabel">Minimum Delegation</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.min_delegation_size}
                  />
                </td>
              </tr>
              <tr>
                <td className="fieldLabel">Maximun Delegation</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.max_delegation_size}
                  />
                </td>
              </tr>
              <tr>
                <th colSpan="2">Primary Contact Information</th>
              </tr>
              <tr>
                <td className="fieldLabel">Name</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.primary_name}
                  />
                </td>
              </tr>
              <tr>
                <td className="fieldLabel">Email</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.primary_email}
                  />
                </td>
              </tr>
              <tr>
                <td className="fieldLabel">Phone</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.primary_phone}
                  />
                </td>
              </tr>
              <tr>
                <th colSpan="2">Secondary Contact Information</th>
              </tr>
              <tr>
                <td className="fieldLabel">Name</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.secondary_name}
                  />
                </td>
              </tr>
              <tr>
                <td className="fieldLabel">Email</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.secondary_email}
                  />
                </td>
              </tr>
              <tr>
                <td className="fieldLabel">Phone</td>
                <td className="field">
                  <input
                    type="text"
                    value={school.secondary_phone}
                  />
                </td>
              </tr>
            </table>
          </div>
          <div className="tablemenu footer">
            Dont forget to save!
          </div>
        </form>
        <br />
        <LogoutButton />
      </InnerView>
    );
  },
});

module.exports = AdvisorProfileView;
