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
var Link = require('rrouter').Link;

var TYPE_CLUB = 1;
var TYPE_CLASS = 2;

var AdvisorProfileView = React.createClass({

  render: function() {
    var user = this.props.user._user;
    var school = user.school;
    return (
      <InnerView>
        <h2> Welcome, <span className="advisorfirstname"> {user.first_name}! </span> </h2>
        <p> We're very excited to see <span className="schoolname"> {school.name} </span> at
        BMUN 63 this year! Here, you can view and edit your registration
        information for the conference, edit your delegate roster, and find
        answers to frequently asked questions. To edit your information, just
        click on any of the highlighted fields and add your changes. Also,
        <span className="bold"> don't forget to save any information you update!</span></p>
        <br></br>
        <p><strong>Important Note:</strong> Please mail all checks to <strong>
        P.O. Box 4306 Berkeley, CA 94704-0306. If you have any other further
        questions contact me at <Link href="mailto:info@bmun.org"> info@bmun.org</Link>
        and I will respond to all requests efficiently. See you soon!</strong></p>
        <br></br>
        <p className="bold">Who is the USG of External this year?
        <br>Under-Secretary General of External Relations, 63rd Session.</br></p>
        <form id="welcomepage">
          <div className="tablemenu header">
            Dont forget to save!
          </div>
          <div id="welcomeinfocontainer" className="table-container">
          <table id="welcomeinfo" className="table highlight-cells">
            <tr>
              <th colSpan='2'> Advisor Information </th>
            </tr>
            <tr>
              <td className="fieldLabel"> First Name </td>
              <td className="field"> <input type="text" value={user.first_name} className="required" /> </td>
            </tr>
            <tr>
              <td className="fieldLabel"> Last Name </td>
              <td className="field"> <input type="text" value={user.last_name} className="required" /> </td>
            </tr>
            <tr>
              <th colSpan="2"> School Information </th>
            </tr>
            <tr>
              <td className="fieldLabel"> Name </td>
              <td className="field"> <input type="text" value={school.name} className="required" /> </td>
            </tr>
            <tr>
              <td className="fieldLabel"> Address </td>
              <td className="field"> <input type="text" value={school.address} className="required" /> </td>
            </tr>
            <tr>
              <td className="fieldLabel"> City </td>
              <td className="field"> <input type="text" value={school.city} className="required" /> </td>
            </tr>
            <tr>
              <td className="fieldLabel"> Zip </td>
              <td className="field"> <input type="text" value={school.zip_code} className="required" /> </td>
            </tr>
            <tr>
              <th colSpan="2"> Program Information </th>
            </tr>
            <tr>
              <td className="fieldLabel"> Program Type </td>
              <td className="field">
                <input type="radio" className="other" name="program_type" value="2"
                  checked={TYPE_CLASS === school.program_type ? "true": "false"} /><label> Class </label>
                <input type="radio" className="other" name="program_type" value="1"
                  checked={TYPE_CLUB === school.program_type ? "true": "false"} /><label> Club </label>
              </td>
            </tr>
            <tr>
              <td className="fieldLabel"> Times Attended </td>
              <td className="field"> <input type="text" value={school.times_attended} className="required IntegersOnly" /> </td>
            </tr>
            <tr>
              <td className="fieldLabel"> Minimum Delegation </td>
              <td className="field"> <input type="text" value={school.min_delegation_size} className="required IntegersOnly" /> </td>
            </tr>
            <tr>
              <td className="fieldLabel"> Maximun Delegation </td>
              <td className="field"> <input type="text" value={school.max_delegation_size} className="required IntegersOnly" /> </td>
            </tr>
            <tr>
              <th colSpan="2">Primary Contact Information </th>
            </tr>
            <tr>
              <td className="fieldLabel"> Name </td>
              <td className="field"> <input type="text" value={school.primary_name} className="required" /> </td>
            </tr>
            <tr>
              <td className="fieldLabel"> Email </td>
              <td className="field"> <input type="text" value={school.primary_email} className="required email" /> </td>
            </tr>
            <tr>
              <td className="fieldLabel"> Phone </td>
              <td className="field"> <input type="text" value={school.primary_phone} className="required phoneNum phoneVal" /> </td>
            </tr>
            <tr>
              <th colSpan="2"> Secondary Contact Information </th>
            </tr>
            <tr>
              <td className="fieldLabel"> Name </td>
              <td className="field"> <input type="text" value={school.secondary_name} className="required" /> </td>
            </tr>
            <tr>
              <td className="fieldLabel"> Email </td>
              <td className="field"> <input type="text" value={school.secondary_email} className="email" /> </td>
            </tr>
            <tr>
              <td className="fieldLabel"> Phone </td>
              <td className="field"> <input type="text" value={school.secondary_phone} className="phoneNum phoneVal" /> </td>
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
