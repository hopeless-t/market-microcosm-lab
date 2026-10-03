# Security Policy

Market Microcosm Lab is a research simulator and does not currently operate a production financial service, user account system, or payment system.

## Reporting a security issue

If you discover a vulnerability that could expose secrets, compromise GitHub Actions, execute untrusted code unexpectedly, or corrupt research evidence, prefer a **private GitHub Security Advisory** for this repository when that feature is available.

Please do not publish exploit details in a public issue before maintainers have had a reasonable opportunity to assess the report.

## Research-integrity issues

Problems such as seed leakage, Oracle leakage, evaluator capture, hidden non-conservation, irreproducible promotion, or stale generated evidence are also treated as security-like integrity failures.

For those, a public **Failure biopsy** issue is appropriate when disclosure itself does not create a software-security risk.

## Scope

Dependency vulnerabilities, CI permission problems, artifact tampering, unsafe deserialization, path traversal, code-execution flaws, and evidence-provenance failures are in scope.

Model disagreement or an unfavorable synthetic result is not a security vulnerability.
