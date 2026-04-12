import os
from typing import Optional, Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI(title="Phone Call Lookup API")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
    raise RuntimeError(
        "Missing TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN environment variables."
    )

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


class CallerNameResult(BaseModel):
    phone_number: str
    valid: bool
    national_format: Optional[str] = None
    country_code: Optional[str] = None
    caller_name: Optional[str] = None
    caller_type: Optional[str] = None
    error: Optional[str] = None


@app.get("/lookup/caller-name", response_model=CallerNameResult)
def lookup_caller_name(
    phone_number: str = Query(..., description="Phone number in E.164 format, e.g. +18135551212"),
) -> CallerNameResult:
    """
    Look up caller name for a phone number using Twilio Lookup v2.
    """
    try:
        result: Any = client.lookups.v2.phone_numbers(phone_number).fetch(
            fields="caller_name"
        )

        caller_name_data = getattr(result, "caller_name", None) or {}

        return CallerNameResult(
            phone_number=getattr(result, "phone_number", phone_number),
            valid=bool(getattr(result, "valid", False)),
            national_format=getattr(result, "national_format", None),
            country_code=getattr(result, "country_code", None),
            caller_name=caller_name_data.get("caller_name"),
            caller_type=caller_name_data.get("caller_type"),
        )

    except TwilioRestException as exc:
        raise HTTPException(
            status_code=exc.status if exc.status else 400,
            detail={
                "message": "Twilio lookup failed",
                "twilio_code": getattr(exc, "code", None),
                "twilio_message": str(exc),
            },
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"message": "Unexpected server error", "error": str(exc)},
        )