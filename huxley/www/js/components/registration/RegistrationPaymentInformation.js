/**
 * Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

 "use strict";

 import React from "react";
 import PropTypes from "prop-types";

// var { PaymentTypes } = require("constants/PaymentTypes");
var { NumberInput } = require("components/NumberInput");
var { _accessSafe } = require("utils/_accessSafe");

 class RegistrationPaymentInformation extends React.Component {
    shouldComponentUpdate(nextProps, nextState) {
        for (let key in this.props.programInformation) {
            if (
            this.props.programInformation[key] !== nextProps.programInformation[key]
            ) {
            return true;
            }
        }

        for (let key in this.props.errors) {
            if (this.props.errors[key] !== nextProps.errors[key]) {
            return true;
            }
        }

        return this.props.programType !== nextProps.programType;
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
                    //value={PaymentTypes.CARD}
                    onChange={this.props.handlepaymentTypeChange}
                    checked={!this.props.paymentType} //TODO: change this to be paymenttypes with constant
                    />{" "}
                    Credit Card
                </label>
                </li>
                <li>
                <label>
                    <input
                    type="radio"
                    //value={PaymentTypes.CHECK}
                    onChange={this.props.handlePaymentTypeChange}
                    checked={this.props.paymentType}
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
    // paymentType: PropTypes.oneOf([PaymentTypes.CHECK, PaymentTypes.CARD]),
  };

export { RegistrationPaymentInformation };