import ollama
from pydantic import BaseModel
from typing import List, Optional
import json

# 1. Define the Strict JSON Schema for the UI
class ClauseAnalysis(BaseModel):
    clause_topic: str
    plain_language_summary: str
    obligations_and_penalties: str
    verifiable_quotes: List[str]
    is_ambiguous: bool
    requires_lawyer_escalation: bool
    warnings: Optional[str]

def analyze_legal_text(contract_text: str, server_ip: str = "http://localhost:11434"):
    """
    Sends the contract text to Gemma 4 and forces a structured JSON response.
    """
    client = ollama.Client(host=server_ip)
    
    # 2. The Master Prompt (Crucial for scoring points)
    system_prompt = """<|think|> You are a private, on-device legal triage assistant. 
    Your job is to analyze legal text and break it down for a non-lawyer.
    
    CRITICAL RULES:
    1. You are NOT a lawyer. You cannot give definitive legal advice.
    2. Separate explicit statements from possible interpretations.
    3. If a clause is vague or jurisdiction-dependent, flag it as ambiguous.
    4. For EVERY claim or summary you make, you MUST extract the exact, verbatim quote from the text to prove it.
    5. If a clause involves severe penalties or highly complex language, flag it for lawyer escalation.
    """

    # 3. Call the Ollama API with schema enforcement
    print("Sending to Gemma 4... (This may take a moment to reason)")
    response = client.chat(
        model='gemma4:e4b',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f"Analyze this contract text:\n\n{contract_text}"}
        ],
        format=ClauseAnalysis.model_json_schema(),
        options={
            'temperature': 0.1, 
        }
    )
    
    # 4. Parse and return the clean JSON
    raw_output = response['message']['content']
    return json.loads(raw_output)

# --- TEST BLOCK ---
if __name__ == "__main__":
    OLLAMA_SERVER = "http://localhost:11434" 
    
    test_contract = """
    4. TERMINATION AND PENALTIES. The Landlord may terminate this lease if the Tenant fails to pay rent within 5 days of the due date. 
    In the event of early termination by the Tenant, the Tenant shall forfeit the entire security deposit and be liable for a $2000 break fee. 
    The Tenant must leave the property in a reasonably clean state.
    """
    
    try:
        result = analyze_legal_text(test_contract, OLLAMA_SERVER)
        print("\n--- FINAL JSON OUTPUT ---")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error connecting to model: {e}")