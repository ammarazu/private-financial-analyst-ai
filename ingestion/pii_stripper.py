from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def strip_pii(text: str) -> dict:
    print("🔒 Scanning for PII...")
    results = analyzer.analyze(text=text, language="en")
    
    if not results:
        print("   ✅ No PII found")
        return {"clean_text": text, "pii_found": [], "count": 0}
    
    pii_types = list(set([r.entity_type for r in results]))
    print(f"   ⚠️  Found PII: {pii_types}")
    
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
    print(f"   ✅ PII stripped successfully")
    
    return {
        "clean_text": anonymized.text,
        "pii_found": pii_types,
        "count": len(results)
    }

if __name__ == "__main__":
    test = """
    John Smith (john@email.com) earned $150,000 in 2024.
    His SSN is 123-45-6789 and phone is 555-867-5309.
    Credit card: 4532-1234-5678-9012
    """
    print("INPUT:", test)
    result = strip_pii(test)
    print("OUTPUT:", result["clean_text"])
    print("PII TYPES FOUND:", result["pii_found"])
    print("TOTAL PII ITEMS:", result["count"])
