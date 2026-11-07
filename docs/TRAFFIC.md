# Archive GitHub repository traffic

GitHub's **Insights → Traffic** displays recent views, unique visitors, clones, and unique cloners. GitHub's traffic API provides a rolling **14-day** window, not an unlimited historical archive.

This optional workflow archives **daily aggregate counts only**, without IP addresses, visitor identities, referrers, notebook data, or account credentials.

## One-time configuration

1. Create a **fine-grained personal access token** restricted to this repository with **Administration: read-only** permission, as required for GitHub's traffic endpoints. Confirm the current permission requirement in [GitHub's traffic API documentation](https://docs.github.com/en/rest/metrics/traffic).
2. In the repository, open **Settings → Secrets and variables → Actions → New repository secret**.
3. Name the secret **TRAFFIC_TOKEN** and paste the token there. **Never commit the token or paste it into an issue or chat.**
4. Open **Actions → Archive GitHub traffic → Run workflow** to test manually. Then inspect the run status.
5. When successful, the scheduled workflow runs once per day and commits aggregate data to [traffic/history.json](../traffic/history.json).

The workflow is intentionally inactive when the secret is missing. A standard `GITHUB_TOKEN` generally does not have the **Administration: read** repository permission required by these traffic endpoints, which is why a separate restricted token is used.

## Stored data

The JSON contains only UTC dates and two daily aggregate metrics:
- `views.count` and `views.uniques`
- `clones.count` and `clones.uniques`

`uniques` is **unique within the reported day**. Adding daily unique counts does **not** give the number of unique people over a month.

GitHub may update recent data after an initial observation. Each run refreshes the available 14-day window. Historical days outside that window remain unchanged.

## Important limitations

- Traffic is not a precise measure of human readership; automated traffic and GitHub filtering may affect the figures.
- If Actions are disabled, the token expires, permissions change, or a scheduled run fails, the archive may have gaps.
- Repository owners and commit metadata remain visible in a public repository even when the archived data is anonymous.
- Fine-grained tokens are sensitive and should be rotated/revoked when no longer needed.
- This is **not** an analytics service that identifies individual visitors.

For a private archive, change the output destination to a private repository or private artifact store **before** enabling the workflow. The example stores aggregate history publicly.
