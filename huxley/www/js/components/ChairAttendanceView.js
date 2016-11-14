/**
* Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
+*/

'use strict';

var React = require('react');
var ReactRouter = require('react-router');

var Button = require('components/Button');
var ConferenceContext = require('components/ConferenceContext');
var CurrentUserStore = require('stores/CurrentUserStore');
var InnerView = require('components/InnerView');
var User = require('utils/User');

var ChairAttendanceView = React.createClass({
  mixins: [
    ReactRouter.History,
  ],

  getInitialState() {
    return {
      assigments: {},
    };
  },

  componentWillMount() {
    var user = CurrentUserStore.getCurrentUser();
    if (!User.isChair(user)) {
      this.history.pushState(null, '/');
    }
  },

  render() {
    return (
      <InnerView>
        <h2>Attendance</h2>
        <p>
          Here you can take attendance for delegates. Note that confirming 
          attendance will alert the advisor as to if there delegates have 
          shown up to committee.
        </p>
          <form>
          <div className="table-container">
            <table className="table highlight-cells">
              <thead>
                <tr>
                  <th>Assignment</th>
                  <th>Present</th>
                  <th>Present2</th>
                  <th>Present3</th>
                </tr>
              </thead>
              <tbody>
                {this.renderAttendanceRows()}
              </tbody>
            </table>
          </div>
          <Button
            color="green">
            Confirm Attendance
          </Button>
        </form>
      </InnerView>
    );
  },

  renderAttendanceRows() {
    /*
     * This will not be used, and is just a dummy example of what the code will
     * look like in the final page
     */
    // return this.state.countries.map(function(country) {
    //   return (
    //     <tr>
    //       <td>
    //         {country.name}
    //       </td>
    //       <td>
    //           <label name="committee_prefs">
    //             <input
    //               className="choice"
    //               type="checkbox"
    //               name="committee_prefs"
    //             />
    //           </label>
    //       </td>
    //       <td>
    //           <label name="committee_prefs">
    //             <input
    //               className="choice"
    //               type="checkbox"
    //               name="committee_prefs"
    //             />
    //           </label>
    //       </td>
    //       <td>
    //           <label name="committee_prefs">
    //             <input
    //               className="choice"
    //               type="checkbox"
    //               name="committee_prefs"
    //             />
    //           </label>
    //       </td>
    //     </tr>
    //   )}.bind(this));
    return (
      <tr></tr>
    );
  },

});
    
module.exports = ChairAttendanceView;
