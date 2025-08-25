# processor.py

import os
import json
from typing import Optional, List
from google import genai
from pydantic import BaseModel, ValidationError


# ---------------- Data Models ---------------- #
class PartyDetails(BaseModel):
    shipowner_name: Optional[str]
    charterer_name: Optional[str]
    port_agent_name: Optional[str]
    confidence: Optional[float]


class CargoDetails(BaseModel):
    operation_type: Optional[str]
    cargo_type: Optional[str]
    quantity: Optional[float]
    unit: Optional[str]
    confidence: Optional[float]


class Signatory(BaseModel):
    role: Optional[str]
    name: Optional[str]
    date_signed: Optional[str]


class DocumentDetails(BaseModel):
    document_source: Optional[str]
    date_of_document: Optional[str]
    port_name: Optional[str]
    vessel_name: Optional[str]
    voyage_number: Optional[str]
    parties: Optional[PartyDetails]
    cargo: Optional[CargoDetails]
    confidence: Optional[float]


class Event(BaseModel):
    event_id: Optional[int]
    event_type: Optional[str]
    start_date: Optional[str]
    start_time: Optional[str]
    end_date: Optional[str]
    end_time: Optional[str]
    duration_hours: Optional[float]
    weather_conditions: Optional[str]
    remarks: Optional[str]
    confidence: Optional[float]


class LaytimeNotes(BaseModel):
    free_time_periods_identified: Optional[str]
    suspension_periods_identified: Optional[str]
    remarks_on_interruptions_or_delays: Optional[str]
    confidence: Optional[float]


class SoFSchema(BaseModel):
    """Represents the structured format for a Statement of Facts document."""
    document_details: DocumentDetails
    events: List[Event]
    laytime_notes: LaytimeNotes
    approvals: Optional[List[Signatory]]


# ---------------- Extraction Logic ---------------- #
def get_structured_data(sof_text: str) -> dict:
    """
    Turn raw Statement of Facts text into structured JSON using Gemini 2.5 Flash.
    Returns a dictionary that matches the SoFSchema.
    """

    print(f"\n[DEBUG] Text length: {len(sof_text)} characters")
    print("[DEBUG] Text preview >>>")
    print(sof_text[:500], "...\n")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY environment variable.")

    try:
        client = genai.Client(api_key=api_key)

        config = {
            "response_mime_type": "application/json",
            "response_schema": SoFSchema,
            "temperature": 0.0,
        }

        prompt = f"""
        You are given a Statement of Facts (SOF) document.
        Extract its details into the provided schema (SoFSchema).

        Guidelines:
        - If information is clearly present, do not leave fields blank.
        - If start and end times are given, calculate duration_hours.
        - Include notes on weather, delays, tug usage, approvals, and laytime.
        - Only leave null if the data is truly missing.

        --- DOCUMENT TEXT ---
        {sof_text}
        --- END DOCUMENT ---
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        print("[DEBUG] Gemini raw output >>>")
        print(response.text, "\n")

        try:
            parsed: SoFSchema = response.parsed
            return parsed.model_dump()

        except ValidationError:
            print("[WARNING] Schema validation failed. Falling back to raw JSON.")
            return json.loads(response.text)

    except Exception as e:
        raw_output = getattr(locals().get("response", None), "text", "No response text available.")
        raise ValueError(
            f"AI data extraction failed. Reason: {e}\n\nRaw Model Output:\n{raw_output}"
        ) from e
