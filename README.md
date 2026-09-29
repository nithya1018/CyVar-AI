# CyVar AI

## AI-Powered Cyber Risk Quantification and Investment Optimization Platform

CyVar AI is a cybersecurity platform that helps organizations understand cyber risk in simple financial terms.

Instead of only showing risks as **Low, Medium, High, or Critical**, CyVar AI combines vulnerability data, threat intelligence, asset importance, security controls, and business context to estimate potential financial losses.

---

## What CyVar AI Does

* Collects asset, vulnerability, and security-control information
* Uses NVD, FIRST EPSS, and CISA KEV for threat intelligence
* Classifies cyber risk using XGBoost
* Uses Monte Carlo Simulation to estimate financial risk
* Calculates Expected Annual Loss (EAL) and Value at Risk (VaR)
* Provides risk monitoring and risk trend analysis
* Allows What-If analysis for security improvements
* Optimizes cybersecurity investments based on a given budget
* Provides compliance and risk reports
* Includes an AI Copilot for cybersecurity insights

---

## Main Features

### Risk Analysis

Combines vulnerabilities, asset criticality, exposure, threat intelligence, and security controls to identify important cyber risks.

### Financial Risk Quantification

Converts technical cyber risks into financial metrics such as:

* Expected Annual Loss (EAL)
* VaR95
* VaR99
* Estimated Financial Exposure

### Threat Intelligence

Uses cybersecurity intelligence from:

* NVD
* FIRST EPSS
* CISA Known Exploited Vulnerabilities (KEV)

These signals help estimate vulnerability exploitation likelihood and prioritize cyber risks.

### What-If Simulator

Allows users to explore how security improvements can affect modeled cyber risk.

For example:

```text
Current Control Strength
        ↓
Improve Security Control
        ↓
Recalculate Risk
        ↓
Compare EAL / VaR
        ↓
Calculate Risk Reduction
```

### Investment Optimizer

Helps identify security controls and investment options that can provide higher modeled risk reduction within a given budget.

### Continuous Risk Monitoring

Tracks risk metrics and changes over time to provide better visibility into the organization's cyber exposure.

### Digital Risk Twin

Provides a visual representation of relationships between:

```text
Business Services
       ↓
Assets
       ↓
Vulnerabilities
       ↓
Cyber Risk
       ↓
Financial Impact
```

### AI Copilot

Provides cybersecurity insights using a locally running AI model connected to CyVar AI context.

---

## Technology Stack

| Component             | Technology                |
| --------------------- | ------------------------- |
| Frontend              | React, Vite               |
| Backend               | FastAPI, Python           |
| Database              | PostgreSQL                |
| Machine Learning      | XGBoost                   |
| Risk Simulation       | Monte Carlo Simulation    |
| Optimization          | PuLP                      |
| AI                    | Ollama + Llama 3.2        |
| Security Intelligence | NVD, FIRST EPSS, CISA KEV |

---

## How It Works

```text
Enterprise / Security Data
          ↓
Assets + Vulnerabilities + Controls
          ↓
Threat Intelligence
(NVD + EPSS + CISA KEV)
          ↓
Risk Analysis + ML
          ↓
Monte Carlo Simulation
          ↓
Financial Risk
(EAL + VaR95 + VaR99)
          ↓
Risk Drivers
          ↓
What-If Analysis
          ↓
Investment Optimization
          ↓
Compliance & Reporting
          ↓
Better Security Decisions
```

---

## Risk Quantification Flow

CyVar AI follows a financial cyber-risk analysis workflow:

```text
Collect Data
     ↓
Normalize Security Information
     ↓
Map Assets to Business Context
     ↓
Analyze Vulnerabilities
     ↓
Evaluate Threat Likelihood
     ↓
Estimate Potential Loss
     ↓
Run Monte Carlo Simulation
     ↓
Calculate EAL / VaR
     ↓
Identify Major Risk Drivers
     ↓
Simulate Security Improvements
     ↓
Optimize Security Investment
```

---

## Cybersecurity Frameworks

CyVar AI supports risk and compliance mapping across:

* NIST Cybersecurity Framework
* ISO/IEC 27001
* CIS Controls
* RBI Cyber Security Framework
* SEBI Cybersecurity and Cyber Resilience Framework

---

## Why CyVar AI?

Traditional cybersecurity risk assessments often communicate risk using categories such as:

```text
Low
Medium
High
Critical
```

These ratings do not clearly communicate the potential financial impact of cyber incidents.

CyVar AI aims to bridge the gap between:

```text
Technical Cybersecurity Data
              ↓
        Cyber Risk Analysis
              ↓
       Financial Risk
              ↓
      Business Decisions
```

This helps organizations understand cyber exposure in measurable financial terms and make more informed security investment decisions.

---

## Expected Benefits

* Better visibility into cyber risk
* Financially quantified risk
* Improved vulnerability prioritization
* Better security investment decisions
* Business-oriented risk communication
* What-If security analysis
* Budget-based investment planning
* Compliance visibility
* Improved risk reporting

---

## Future Enhancements

Planned extensions include:

* SIEM integrations
* EDR integrations
* IAM integrations
* CSPM integrations
* Additional threat-intelligence feeds
* Automated AI mitigation recommendations
* Advanced natural-language risk queries
* Advanced threat prediction
* Additional regulatory frameworks
* Cloud-scale enterprise deployment

---

## Smart India Hackathon 2026

**Problem Statement:** SIH26105

**Title:** AI-Powered Continuous Cyber Risk Quantification and Investment Optimization Platform

**Theme:** Blockchain & Cyber-Security

**Team:** CYBER-CHUNKS

---

## Project Status

CyVar AI currently demonstrates the core cyber-risk quantification workflow through:

* Risk Dashboard
* Vulnerability Intelligence
* XGBoost Risk Analysis
* Monte Carlo Simulation
* EAL and VaR Calculation
* Digital Risk Twin
* What-If Simulation
* Investment Optimization
* Compliance Mapping
* Executive Risk Reporting
* AI Copilot

Enterprise security integrations such as SIEM, EDR, IAM, and CSPM are designed as an extensible integration layer for future deployment.

---

## Disclaimer

CyVar AI is a cybersecurity risk analysis and decision-support prototype.

Financial risk values generated by the platform are modeled estimates and should not be treated as guaranteed predictions of actual financial losses.
