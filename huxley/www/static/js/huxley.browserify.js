/**
 * Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 *
 * @jsx React.DOM
 */

require('jquery.cookie');

var $ = require('jquery');
var React = require('react');
var Router = require('react-router-component');

var Huxley = require('./huxley/Huxley');

var Locations = Router.Locations;
var Location = Router.Location;

$(function() {
  React.renderComponent(
    <Locations>
      <Location path="/www/*" handler={Huxley} />
    </Locations>,
    document.body
  );
});

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
      // TODO: check that it's same origin.
      xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
    }
  }
});
