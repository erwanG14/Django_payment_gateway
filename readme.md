# Django Payment Gateway

A Django-based proof-of-concept payment gateway that simulates the interaction between an online merchant, a payment gateway, and a bank system.

The goal of this project is to better understand how payment workflows work behind the scenes, including payment session creation, transaction processing, bank verification, and payment success or failure handling.

## Project Overview

This project is structured around three main components:

- **Merchant website (`site_marchand`)**: displays products and initiates payment sessions.
- **Payment gateway (`gateway`)**: receives payment requests, manages payment sessions, stores transaction data, and redirects users to the payment flow.
- **Bank service (`banque`)**: simulates bank-side verification of cardholder information and account balance.

## Features

- Product catalogue and payment initiation from a merchant website
- Payment session creation with an idempotency key
- Token-based payment flow between the merchant and the gateway
- Transaction creation and status management
- Simulated bank verification for card data and account balance
- Success and failure payment pages
- Basic request signing using HMAC and timestamps
- Django models with uniqueness constraints for clients, cards, and payment sessions

## Tech Stack

- Python
- Django
- SQLite
- HTML
- Requests
- HMAC / SHA-256 for request signature verification

## Main Applications

### `site_marchand`

Simulates an e-commerce website where users can browse products and start a payment process.

Main responsibilities:

- Display product catalogue
- Create a payment session
- Send the session to the payment gateway
- Redirect the user to the payment page
- Display payment success or failure pages

### `gateway`

Acts as the payment gateway between the merchant and the bank.

Main responsibilities:

- Receive payment session requests from the merchant
- Generate and manage payment sessions
- Store clients, cards, tokens, and transactions
- Forward transaction data to the bank service
- Handle payment success or failure responses

### `banque`

Simulates a banking system.

Main responsibilities:

- Verify client and card information
- Check account balance
- Accept or refuse a transaction
- Validate signed requests from the gateway

## Payment Flow

1. The user selects a product on the merchant website.
2. The merchant creates a payment session and sends it to the gateway.
3. The gateway returns a payment URL.
4. The user is redirected to the payment page.
5. The user enters payment information.
6. The gateway creates a transaction and sends it to the bank service.
7. The bank verifies the account and either accepts or refuses the payment.
8. The user is redirected to a success or failure page.

