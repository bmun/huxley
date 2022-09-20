/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

 "use strict";

import React from "react";
import PropTypes from "prop-types";

var { PaymentTypes } = require("constants/PaymentTypes");
var { NumberInput } = require("components/NumberInput");
var { _accessSafe } = require("utils/_accessSafe");

 class RegistrationPaymentInformation extends React.Component {
    shouldComponentUpdate(nextProps, nextState) {
        for (let key in this.props.paymentInformation) {
            if (
            this.props.paymentInformation[key] !== nextProps.paymentInformation[key]
            ) {
            return true;
            }
        }

        for (let key in this.props.errors) {
            if (this.props.errors[key] !== nextProps.errors[key]) {
            return true;
            }
        }

        return this.props.paymentType !== nextProps.paymentType;
    }

    render() {
        var accessErrors = _accessSafe.bind(this, this.props.errors);
        var accessHandlers = _accessSafe.bind(this, this.props.handlers);
        var accessPaymentType = _accessSafe.bind(this, this.props.paymentInformation);
        return (
            <div id="payment_information">
            <h3>Payment Information</h3>
            <p className="instructions">How will you be making your payment?</p>
            <ul>
                <li>
                <label>
                    <input
                    type="radio"
                    value={PaymentTypes.CARD}
                    onChange={this.props.handlePaymentTypeChange}
                    checked={this.props.paymentType == PaymentTypes.CARD}
                    />{" "}
                    Credit Card
                </label>
                </li>

                <li>
                <label>
                    <input
                    type="radio"
                    value={PaymentTypes.CHECK}s
                    onChange={this.props.handlePaymentTypeChange}
                    checked={this.props.paymentType == PaymentTypes.CHECK}
                    />{" "}
                    Check
                </label>
                </li>
            </ul>
            </div>
        );
    }
}

RegistrationPaymentInformation.propTypes = {
    handlers: PropTypes.object,
    errors: PropTypes.object,
    paymentInformation: PropTypes.object,
    handlePaymentTypeChange: PropTypes.func,
    paymentType: PropTypes.oneOf([PaymentTypes.CARD, PaymentTypes.CHECK]),
  };

export { RegistrationPaymentInformation };