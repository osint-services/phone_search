# Twilio Caller Name Lookup API

A small FastAPI microservice that resolves caller name information for a phone number using Twilio Lookup v2.

## Overview
This service exposes a single endpoint to look up caller name metadata for a phone number in E.164 format.

## Requirements
- Python 3.9 or higher
- Twilio account with Lookup API access

## Environment Variables
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`

The service will fail to start if either environment variable is missing.

## Tech Stack
- FastAPI
- Uvicorn
- Twilio Python SDK
- Pydantic

## Setup
1. Create a Python virtual environment:
   `python -m venv venv`
2. Activate it:
   `source venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Set your Twilio credentials:
   `export TWILIO_ACCOUNT_SID=your_sid`
   `export TWILIO_AUTH_TOKEN=your_token`
5. Start the server:
   `uvicorn server:app --reload`

## Endpoint
- GET `/lookup/caller-name?phone_number={phone_number}`
  - Query parameter: `phone_number` in E.164 format, e.g. `+18135551212`
  - Returns caller name metadata for the requested phone number.

## Example Response
```json
{
  "phone_number": "+18135551212",
  "valid": true,
  "national_format": "+1 813-555-1212",
  "country_code": "US",
  "caller_name": "SCAM ALERT",
  "caller_type": "business",
  "error": null
}
```

## Notes
- The current implementation uses `twilio.rest.Client` and Twilio Lookup v2.
- Errors from Twilio are returned as HTTP errors with a JSON detail payload.
