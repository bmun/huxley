/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var LinkedStateMixin = require('react-addons-linked-state-mixin');
var React = require('react');

var Button = require('./Button');
var InnerView = require('./InnerView');
var LogoutButton = require('./LogoutButton');
var ConferenceContext = require('./ConferenceContext');
var ProgramTypes = require('../constants/ProgramTypes');
var User = require('../utils/User');

var AdvisorProfileView = React.createClass({
  mixins: [LinkedStateMixin],

  propTypes: {
    user: React.PropTypes.object.isRequired
  },

  contextTypes: {
    conference: React.PropTypes.shape(ConferenceContext)
  },

  render: function() {
    var conference = this.context.conference;
    var user = this.props.user;
    var school = User.getSchool(user);
    var invoiceUrl = '/api/schools/' + school.id + '/invoice/';
    return (
      <InnerView>
        <h2>Welcome, {user.first_name}!</h2>
        <p>
          We are very excited to see {school.name} at BMUN {conference.session} this year! Here,
          you can view your registration information for the conference. Please
          note that fees are currently <strong>estimates</strong> based on the
          approximate delegation size given during registration.
        </p>
        <br />
        <p>
          Advisors, if you wish to generate an invoice for your school with your
          payment details, please click on the Generate Your Invoice button under
          the Fees tab. You will receive an invoice in your email within 2 business
          days.
        </p>
        <br />
        <p><strong>Important Note:</strong> Please mail all checks to <strong>
        P.O. Box 4306 Berkeley, CA 94704-0306. If you have any other further
        questions contact me at <a href="mailto:info@bmun.org">
        info@bmun.org</a> and I will respond to all requests efficiently.
        See you soon!</strong></p>
        <br />
        <p><strong>{conference.external}
        <br />
        Under-Secretary General of External Relations, {conference.session}th Session.</strong></p>
        <form id="welcomepage">
          <div className="tablemenu header">
          </div>
          <div id="welcomeinfocontainer" className="table-container">
            <table id="welcomeinfo" className="table highlight-cells">
              <thead>
                <tr>
                  <th colSpan="2">Advisor Information</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="fieldLabel">First Name</td>
                  <td className="field">
                    {user.first_name}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Last Name</td>
                  <td className="field">
                    {user.last_name}
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">School Information</th>
                </tr>
                <tr>
                  <td className="fieldLabel">Name</td>
                  <td className="field">
                    {school.name}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Address</td>
                  <td className="field">
                    {school.address}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">City</td>
                  <td className="field">
                    {school.city}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Zip</td>
                  <td className="field">
                    {school.zip_code}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Waitlisted</td>
                  <td className="field">
                    {school.waitlist == true ? 'Yes' : 'No'}
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">Program Information</th>
                </tr>
                <tr>
                  <td className="fieldLabel">Program Type</td>
                  <td className="field">
                    {school.program_type === 1 ? 'Club' : 'Class'}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Times Attended</td>
                  <td className="field">
                    {school.times_attended}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Number of Beginner Delegates</td>
                  <td className="field">
                    {school.beginner_delegates}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Number of Intermediate Delegates</td>
                  <td className="field">
                    {school.intermediate_delegates}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Number of Advanced Delegates</td>
                  <td className="field">
                    {school.advanced_delegates}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Number of Spanish Speaking
                  Delegates</td>
                  <td className="field">
                    {school.spanish_speaking_delegates}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Number of Chinese Speaking
                  Delegates</td>
                  <td className="field">
                    {school.chinese_speaking_delegates}
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">Primary Contact Information</th>
                </tr>
                <tr>
                  <td className="fieldLabel">Name</td>
                  <td className="field">
                    {school.primary_name}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Email</td>
                  <td className="field">
                    {school.primary_email}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Phone</td>
                  <td className="field">
                    {school.primary_phone}
                  </td>
                </tr>
                <tr>
                  <th colSpan="2">Secondary Contact Information</th>
                </tr>
                <tr>
                  <td className="fieldLabel">Name</td>
                  <td className="field">
                    {school.secondary_name}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Email</td>
                  <td className="field">
                    {school.secondary_email}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Phone</td>
                  <td className="field">
                    {school.secondary_phone}
                  </td>
                </tr>
                <tr>
                  <th>Fees</th>
                  <td className="field">
                    <a className="button button-green" href={invoiceUrl} target="_blank">
                      Generate Your Invoice
                    </a>
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Fees Owed</td>
                  <td className="field">
                    {'$' + school.fees_owed.toFixed(2)}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Fees Paid</td>
                  <td className="field">
                    {'$' + school.fees_paid.toFixed(2)}
                  </td>
                </tr>
                <tr>
                  <td className="fieldLabel">Balance</td>
                  <td className="field">
                    {'$' + (school.fees_owed - school.fees_paid).toFixed(2)}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="tablemenu footer">
          </div>
        </form>
      </InnerView>
    );
  },
});
module.exports = AdvisorProfileView;
