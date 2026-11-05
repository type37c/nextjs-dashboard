# Hosted CI and local validation

Checked on 2026-11-05.

The initial [GitHub Actions run](https://github.com/type37c/nextjs-dashboard/actions/runs/42013472860) failed **before any job step started**. GitHub's check annotation reports an account-level runner-start restriction. No test or dependency-installation step ran, so that result does not identify a code failure. The repository owner must resolve the account restriction before hosted validation can execute. A green hosted CI result has not been obtained.

The workflow remains enabled. After resolving the restriction, rerun the failed job or use its manual `workflow_dispatch` trigger. If that run encounters a code or environment error, investigate its actual logs rather than treating the local result as a substitute.

Local evidence is separate:

- Saved-data audit: all 1,152 trial scores, 64 old queries, source hashes, eligibility/error boundaries and two radial trace reconstructions passed.
- Full same-input acquisition: trial and old-query records matched exactly; state differences were bounded by approximately 4.1e-14. See [validation JSON](RELEASE_VALIDATION.json).
- The stored traces were not all bitwise identical, and this was not confirmation on independent scientific conditions.
