# rais-ecfr

Live access to the Electronic Code of Federal Regulations for research administration. Grounds answers about 2 CFR 200 (Uniform Guidance), 45 CFR 46 (Common Rule), procurement standards and indirect costs in the current regulatory text instead of recollection, and can compare a section across two dates.

**Owner** Cornell RAIS. **Status** published. **Version** 0.1.0.

## What is inside

- Skill `ecfr-guidance`: when to reach for the regulation, which eCFR tool to call, how to cite.
- Connector `ecfr` (`.mcp.json`): the AI4RA eCFR MCP server (University of Idaho). On Cornell gateway machines the same server is already provided through managed policy with tool approvals pre-set; the managed entry wins when both are present, so the skill works either way.

## Notes

- Tool names carry the prefix `ecfr_mcp_server_`. The AI4RA documentation lists them without the prefix.
- The hosted server occasionally reports "Connection to server failed." Retry; it clears within a minute.

Source and credit: https://ai4ra.github.io/mcp-ecfr
