# GitHub and Autobot monitoring

The `Repository health monitor` workflow runs every six hours and can also be
started manually. It discovers **all** repositories belonging to the profile,
reports their last push and latest GitHub Actions result, and visibly marks the
repository named `Autobot` (matching is case-insensitive).

## One-time setup

1. Push this repository and enable GitHub Actions if it is disabled.
2. For public repositories, no additional secret is required.
3. To include private repositories, create a fine-grained personal access token
   with read access to **Actions** and **Metadata** for every repository to be
   watched. Save it in this repository as the Actions secret
   `ALL_REPOS_MONITOR_TOKEN`.
4. Open **Actions → Repository health monitor → Run workflow** to verify the
   report immediately. Each scheduled run also stores the Markdown report as a
   30-day artifact.

Run the same check locally after authenticating GitHub CLI:

```bash
gh auth login
GH_TOKEN="$(gh auth token)" python scripts/monitor_github.py --owner JungyulPark
```

An unauthenticated run can inspect public repositories, but it is subject to
GitHub's low anonymous API rate limit.

## Higgsfield MCP status

No Higgsfield MCP endpoint or credentials are stored in this repository. Do not
guess an endpoint or commit an API key. A connection can only be configured
after Higgsfield supplies an official MCP server URL (or an official local
server command) and the corresponding credential. Add that server to the MCP
client's user-level configuration, keep its key in an environment variable,
then confirm it by listing the server's tools/resources. This avoids exposing a
credential in Git while making the missing prerequisite explicit.
