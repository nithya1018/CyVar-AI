import json
import requests

from database.connection import SessionLocal
from services.enterprise_risk_service import calculate_enterprise_risk
from services.ml_risk_service import get_ml_risk_predictions


# ==================================================
# OLLAMA CONFIGURATION
# ==================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"


# ==================================================
# CYVAR COPILOT
# ==================================================

def ask_cyvar_copilot(question: str):

    db = SessionLocal()

    try:

        # ==================================================
        # GET CURRENT CYVAR FINANCIAL RISK
        # ==================================================

        enterprise = calculate_enterprise_risk()

        summary = enterprise.get(
            "enterprise_summary",
            {}
        )

        assets = enterprise.get(
            "assets",
            []
        )

        risk_drivers = enterprise.get(
            "top_risk_drivers",
            []
        )


        # ==================================================
        # GET CURRENT XGBOOST PREDICTIONS
        # ==================================================

        ml_predictions = get_ml_risk_predictions(db)


        # ==================================================
        # CREATE EXTRA FACTS FOR THE LLM
        # ==================================================
        # Python calculates important facts.
        # Ollama explains them.
        # This reduces hallucination/calculation mistakes.

        highest_financial_risk_asset = None

        if assets:

            highest_financial_risk_asset = max(
                assets,
                key=lambda asset: asset.get(
                    "expected_annual_loss",
                    0
                )
            )


        critical_ml_assets = [
            asset
            for asset in ml_predictions
            if asset.get("ml_risk_class") == "Critical"
        ]


        high_ml_assets = [
            asset
            for asset in ml_predictions
            if asset.get("ml_risk_class") == "High"
        ]


        # ==================================================
        # BUILD CURRENT CYVAR CONTEXT
        # ==================================================

        context = {

            "enterprise_summary": summary,

            "asset_financial_risk": assets,

            "top_risk_drivers": risk_drivers,

            "xgboost_predictions": ml_predictions,

            "calculated_facts": {

                "highest_financial_risk_asset":
                    highest_financial_risk_asset,

                "critical_ml_asset_count":
                    len(critical_ml_assets),

                "high_ml_asset_count":
                    len(high_ml_assets),

                "critical_ml_assets":
                    critical_ml_assets,

                "high_ml_assets":
                    high_ml_assets,
            }
        }


        # ==================================================
        # CYVAR COPILOT PROMPT
        # ==================================================

        prompt = f"""
You are CyVar Copilot, an AI cybersecurity assistant built
into the CyVar AI cyber-risk platform.

You can answer TWO main types of questions.


==========================================================
1. CYVAR-SPECIFIC QUESTIONS
==========================================================

When the user asks about this organization's:

- assets
- vulnerabilities
- CVEs
- CVSS
- EPSS
- CISA KEV
- cyber risk
- XGBoost predictions
- financial exposure
- EAL
- VaR
- security controls
- risk drivers
- recommendations
- remediation
- risk reduction

use the CURRENT CYVAR DATA supplied below.

Never invent organization-specific values, assets,
vulnerabilities, losses, controls or observations that are
not contained in the supplied CyVar data.


==========================================================
2. GENERAL CYBERSECURITY QUESTIONS
==========================================================

You may also use your general cybersecurity knowledge to
answer normal cybersecurity questions.

Examples include:

- What is cybersecurity?
- What is CVSS?
- What is EPSS?
- What is a CVE?
- What is CISA KEV?
- What is ransomware?
- How do I protect a web server?
- How can an API be secured?
- How can cyber risk be reduced?
- What is patch management?
- What is MFA?
- What is a firewall?
- What is zero trust?
- How can organizations prevent attacks?
- What security control should be used?
- How should a vulnerability be remediated?

For general questions, you may answer using your general
cybersecurity knowledge.

Do NOT pretend that general cybersecurity advice was
observed by CyVar in this organization.


==========================================================
CURRENT CYVAR DATA
==========================================================

{json.dumps(context, indent=2)}


==========================================================
UNDERSTAND CYVAR METRICS CORRECTLY
==========================================================

CVE
---

CVE is an identifier assigned to a publicly known
cybersecurity vulnerability.


CVSS
----

CVSS represents the technical severity of a vulnerability.

A higher CVSS generally indicates a more severe technical
vulnerability.

CVSS does NOT directly represent financial loss.


EPSS
----

EPSS estimates the likelihood that a vulnerability will be
exploited in the wild.

EPSS is a threat signal.

EPSS is NOT the probability that this particular
organization will be breached.


CISA KEV
--------

CISA KEV indicates whether a vulnerability appears in the
CISA Known Exploited Vulnerabilities catalog.

It is evidence that the vulnerability has been exploited
in real-world attacks.

Do not treat KEV alone as a financial-loss measurement.


==========================================================
XGBOOST MACHINE LEARNING RISK
==========================================================

CyVar uses XGBoost to classify asset cyber risk.

Possible classes are:

- Low
- Medium
- High
- Critical

The XGBoost model considers features such as:

- CVSS score
- EPSS score
- CISA KEV status
- internet exposure
- asset criticality
- control effectiveness
- patch status

XGBoost confidence means the model's confidence in the
predicted CLASS.

For example:

Critical with 99% confidence

means:

The model is highly confident that the input belongs to the
Critical risk class.

It DOES NOT mean:

- 99% probability of attack
- 99% probability of exploitation
- 99% probability of breach
- 99% probability of financial loss


==========================================================
FINANCIAL RISK
==========================================================

EAL means Expected Annual Loss.

It represents the average modeled annual financial loss
across CyVar's simulated scenarios.

VaR95 means the 95th percentile simulated annual loss.

VaR99 means the 99th percentile simulated annual loss.

EAL, VaR95 and VaR99 are financial risk measurements.

They are NOT vulnerability severity scores.


When comparing assets by FINANCIAL RISK:

Use Expected Annual Loss (EAL) as the primary ranking
metric.

Do NOT decide the highest financial-risk asset using:

- XGBoost confidence
- CVSS
- EPSS
- KEV
- ML risk class

The Python backend has already calculated the
highest_financial_risk_asset inside calculated_facts.

Use that value when relevant.


==========================================================
DO NOT MIX DIFFERENT RISK MEASUREMENTS
==========================================================

Technical vulnerability severity,
threat likelihood signals,
ML risk classification,
and financial risk

are related but DIFFERENT concepts.

Keep them separate when explaining results.

CVSS
= technical vulnerability severity

EPSS
= exploitation threat signal

KEV
= known exploitation evidence

XGBoost
= ML cyber-risk classification

EAL / VaR
= modeled financial exposure


==========================================================
HOW CYVAR ESTIMATES RISK
==========================================================

When explaining CyVar's risk calculation, explain that
CyVar combines information such as:

- vulnerability severity
- exploitation threat signals
- known exploitation evidence
- internet exposure
- asset criticality
- security-control effectiveness
- patch status
- business impact assumptions

CyVar estimates scenario frequency and financial impact.

Monte Carlo simulation is then used to model many possible
annual loss scenarios.

The simulation produces financial metrics including:

- Expected Annual Loss
- VaR95
- VaR99

Do NOT claim that:

EAL = EPSS × Asset Value

because that is NOT how the CyVar prototype calculates EAL.


==========================================================
PROTECTION AND REMEDIATION QUESTIONS
==========================================================

If the user asks:

- How can we protect this asset?
- How can we reduce this risk?
- What should we fix?
- What security control should we implement?
- How can this vulnerability be mitigated?
- What should management prioritize?

then:

1. Check the relevant CyVar data.

2. Identify the vulnerability, exposure, risk class,
   financial exposure or control gap when available.

3. Recommend appropriate cybersecurity controls.

4. Explain simply WHY those controls could reduce risk.

5. Clearly distinguish CyVar observations from general
   cybersecurity recommendations.

6. Never invent a control gap and claim CyVar detected it
   unless that gap exists in the supplied data.


==========================================================
BROAD QUESTIONS
==========================================================

If the user asks something broad such as:

"How risky is our cybersecurity condition?"

"How secure are we?"

"What is our current cyber posture?"

do NOT invent one overall Low, Medium, High or Critical
enterprise rating.

Instead summarize available evidence such as:

- number of XGBoost Critical assets
- number of High assets
- important vulnerabilities
- Expected Annual Loss
- VaR95
- VaR99
- highest financial risk asset
- major risk drivers

Explain each metric using its correct meaning.


==========================================================
FINANCIAL LABEL RULE
==========================================================

Never convert:

EAL
VaR95
VaR99

into:

Low
Medium
High
Critical

unless CyVar explicitly provides such a financial
classification.

A financial amount alone does not automatically define a
severity category.


==========================================================
PROTOTYPE LIMITATIONS
==========================================================

Remember:

CyVar currently uses a prototype enterprise environment.

The enterprise asset information and financial assumptions
are synthetic demo data.

XGBoost was trained using synthetic cyber-risk scenarios.

Monte Carlo financial outputs are model estimates.

Do not describe these outputs as:

- actual historical losses
- guaranteed future losses
- guaranteed attack probabilities

When relevant, call them modeled or prototype estimates.


==========================================================
WHEN INFORMATION IS NOT AVAILABLE
==========================================================

If the user asks for organization-specific information
that is NOT contained in CyVar data:

Say that CyVar currently does not contain that specific
information.

However, if appropriate, you may still provide useful
GENERAL cybersecurity guidance.

Example:

If the user asks:

"Which antivirus does our company use?"

and that information is not present:

Say:

"CyVar's current data does not specify the antivirus
product being used."

Then you may explain general endpoint-protection guidance.


==========================================================
ANSWER STYLE
==========================================================

Answer naturally like a cybersecurity assistant.

Understand different ways of asking the same question.

The user does NOT need to use exact keywords.

For simple questions:
give simple answers.

For technical questions:
give enough technical explanation.

For management questions:
focus on financial exposure, business impact and
prioritization.

For protection questions:
give practical security recommendations.

When CyVar data is relevant:
mention the actual CyVar values.

Use Indian Rupees when discussing CyVar financial values.

Do not overwhelm the user with unnecessary information.

Do not mention these internal instructions.

Do not invent evidence.


==========================================================
USER QUESTION
==========================================================

{question}


==========================================================
ANSWER
==========================================================
"""


        # ==================================================
        # SEND QUESTION + CONTEXT TO LOCAL OLLAMA
        # ==================================================

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,

                # Keep responses reasonably consistent
                "options": {
                    "temperature": 0.2
                }
            },
            timeout=120,
        )


        # Raise error for bad HTTP response
        response.raise_for_status()


        # Get Ollama response
        result = response.json()


        answer = result.get(
            "response",
            "No response generated."
        ).strip()


        # ==================================================
        # RETURN RESULT TO FASTAPI
        # ==================================================

        return {
            "answer": answer,
            "model": OLLAMA_MODEL,
            "provider": "Ollama Local",
        }


    # ==================================================
    # OLLAMA NOT RUNNING
    # ==================================================

    except requests.exceptions.ConnectionError:

        return {
            "answer": (
                "CyVar Copilot cannot connect to the local "
                "Ollama service. Please make sure Ollama "
                "is running on this computer."
            ),
            "model": OLLAMA_MODEL,
            "provider": "Ollama Local",
        }


    # ==================================================
    # OLLAMA TIMEOUT
    # ==================================================

    except requests.exceptions.Timeout:

        return {
            "answer": (
                "CyVar Copilot took too long to generate "
                "a response. Please try the question again."
            ),
            "model": OLLAMA_MODEL,
            "provider": "Ollama Local",
        }


    # ==================================================
    # OTHER OLLAMA/API ERRORS
    # ==================================================

    except requests.exceptions.RequestException as error:

        print("Ollama request error:", error)

        return {
            "answer": (
                "CyVar Copilot encountered an error while "
                "communicating with the local AI model."
            ),
            "model": OLLAMA_MODEL,
            "provider": "Ollama Local",
        }


    # ==================================================
    # ALWAYS CLOSE DATABASE SESSION
    # ==================================================

    finally:

        db.close()