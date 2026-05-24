---
type: reference
version: 4
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
workstream: null
tags: [permissions, customer-1, m365, box, smartsheet]
---

**ITS — Permissions Ask v4**

*Box section rewritten under OAuth User Authentication. M365 + Smartsheet sections unchanged.*

*2026-05-20*

# Scope of This Doc

*This doc applies to the cutover from sandbox to live customer tenants. Sandbox build is self-administered — Solution Smith has full admin on his own sandbox tenants by definition. The asks below are what**'**s needed in the customer**'**s live M365, Smartsheet, and Box tenants at cutover time, not before.*

**When this conversation happens: **at the Phase 1 → 1.5 gate, when the full ITS system (all five workstreams + Tier 3 ship surfaces) has been processing real reports under permanent human review in sandbox for 30 consecutive days and the owner is ready to cut over to live tenants.

**Why this is at the right time, not before: **the 2026-05-13 sandbox-first pivot eliminated the dependency on live-tenant admin grants for the build phase. The asks below are cutover-phase needs.

# Shape of the Ask

Each system has a one-time setup that needs admin access, then ongoing operation that doesn't. The ask is admin-equivalent access in M365 and Smartsheet so cutover can happen without bottlenecking on the owner. Box has a simpler ask under the new OAuth-based auth method (see Box section below). None of these touch billing, payroll, or personal data. Each has a documented minimum-access fallback if the owner would rather keep the access below admin — the cost of the fallback is owner time, not security.

# Summary

**Microsoft 365: **Application Administrator + Cloud Application Administrator (Entra ID). Teams Administrator confirmed (Teams bot path for ITS Chat per V&R v7).

**Smartsheet: **System Admin on the customer's plan. Three workspaces require provisioning at cutover.

**Box: **standard user account (no admin role required) with collaborator access on ITS-relevant folders. **Substantially simpler than the v3 ask** — Co-Admin requirement removed. See expanded section below for the architectural reason.

# Microsoft 365 — Outlook, Teams, Graph API

ITS authenticates as a registered application in Entra ID. Scripts call the Microsoft Graph API as the app — they do not log in as a person.

**What I****'****m asking for**

Two Entra ID roles: Application Administrator and Cloud Application Administrator. Plus Teams Administrator for the Teams bot path (ITS Chat).

**Why**

Application Administrator lets me register the ITS app and configure its credentials. Cloud Application Administrator lets me grant tenant-wide consent for the specific Graph permissions the app needs (read mail, send mail, post to Teams). Teams Administrator lets me deploy the custom Teams app and manage Teams messaging policies. Without these, every new permission or new workstream becomes a meeting.

**What this lets me touch**

- Register, configure, and delete Entra ID applications (the ITS app and any future ones)

- Grant tenant-wide consent for specific Graph API permission scopes on apps I created

- Read app client IDs and rotate app secrets

- With Teams Admin: deploy custom Teams apps and manage Teams messaging policies

**What this does NOT let me touch**

- Billing, license assignments, or payment methods

- Creating, deleting, or resetting passwords for user accounts (that's User Administrator)

- Anyone's personal mailbox content directly

- Security policies, conditional access, or compliance / DLP settings

- SharePoint, OneDrive, or Office document content

- Global-Administrator-only actions (tenant identity, directory sync, domain changes)

**If you****'****d rather keep me below admin**

You stay Global Administrator and run the one-time app registration and consent yourself, following a written recipe I provide. Adds about 30 minutes of your time per workstream that needs new permissions.

**Also needed regardless of my role**

- Shared mailboxes (safety@, procurement@, subcontracts@, info@, ops@, voice@, its@) created by an admin

- Full Access + Send As permissions granted to the ITS app on those mailboxes

- Exchange Online ServicePrincipal created via PowerShell after Entra app registration (see Handover Plan v6.1 Step 4 — this is a non-obvious requirement that surfaces as HTTP 403 [RAOP] if missed)

# Smartsheet

ITS reads from and writes to **multiple sheets across three workspaces**, separated by audience: customer day-to-day, customer-employee approval surfaces, and operator-only system surfaces. The three workspaces require different access tiers from the operator perspective at cutover, but a single account-level admin grant (System Admin) covers all the provisioning work.

**What I****'****m asking for**

System Admin on the customer's Smartsheet plan.

**Why**

Need to create the three workspaces (System, Human Review, customer-facing portfolio), provision sheets and schemas, add and rename columns, manage workspace sharing, and create the ITS service-account user that holds the API token. System Admin is the only role that can do all of those without owner-in-loop.

## §3.1 Three-workspace provisioning at cutover

ITS uses a three-workspace audience-tiered topology to make the operator vs customer-employee access boundary visible and enforceable. Each workspace serves a different audience and gets different access at cutover.

- **Forefront Portfolio — ITS Demo (customer-facing portfolio). **Day-to-day project visibility for PMs and admins. PMs need EDITOR; no operator-system access required from here.

- **ITS — Human Review (customer-employee approvers). **Per-workstream Pending_Review sheets where approvers sign off on AI-generated content. Approvers scoped to their workstream's subfolder only.

- **ITS — System (operator-only). **Config rows, error log, review queue, quarantine, time-off sheet. Solution Smith retains ADMIN here for ongoing maintenance.

Separating these workspaces makes the access boundary visible and enforceable.

## §3.2 Customer-side Smartsheet access grants (post-cutover)

For Evergreen-employee access on the live tenants after cutover:

- **PMs and admins **(day-to-day operators on customer projects): EDITOR on the customer portfolio workspace; no access to ITS — System.

- **Approvers **(Teala, Sam, Jacob for Safety Reports; similar approver designations for other workstreams as they're built): EDITOR on the relevant subfolder of ITS — Human Review only. Approver granted access to 01 — Safety Reports for WPR; 02 — Subcontracts for executed contracts; etc. Approvers do NOT get blanket Human Review access — workstream-scoped.

- **Personnel admins: **EDITOR on ITS — Human Review / 06 — Personnel (for ITS_Time_Off updates). No other Human Review subfolder access required.

- **Trained maintainer at customer (when one exists): **ADMIN on ITS — System workspace. This is a graduation event; not granted at initial cutover. Solution Smith remains primary operator until the customer has a trained maintainer in place.

**If you****'****d rather keep me below admin**

I stay a regular user; you share each ITS-touched workspace and sheet with me as Admin individually, and you create the service-account user. Works, but every new workstream and every new sheet adds a sharing request to your plate. Three workspaces × many sheets means the fallback is meaningfully more owner-time-consuming than the M365 fallback.

# Box

ITS authenticates to Box via OAuth 2.0 User Authentication. This is a substantive change from v3, which assumed JWT / Server Authentication acting through a Box Platform App. The JWT path was evaluated and declined; see **Why this changed in v4** below for the architectural reasoning.

## What I'm asking for

**A standard Box user account** on the customer's Box enterprise tenant, dedicated to ITS (e.g., *its@evergreenrenewables.com*), with collaborator access on the folders ITS needs to read from and write to.

No admin role required. No Co-Admin. No Box Platform add-on. The user account is provisioned the same way any new Box user is provisioned — single seat on the existing Enterprise plan.

## Why

ITS uses OAuth 2.0 Authorization Code Grant against a Box Custom App configured for User Authentication. The Custom App can be created by any Box user in their own Developer Console (no admin action needed). The app is authorized via the standard OAuth consent flow when ITS first authenticates — the dedicated ITS user consents to its own scopes; no enterprise admin is in the loop. Subsequent ITS runs use the rotating refresh token stored in macOS Keychain. The whole setup completes in ~5 minutes once the user account is provisioned.

## What this lets ITS touch

- Read and write folders and files the ITS user has been granted collaborator access to

- Search across content the ITS user can see

- Read folder/file metadata visible to the ITS user

## What this does NOT let ITS touch

- Billing, payment methods, or licensing

- Other users' content (Box enforces the same access boundary the human ITS user would have)

- Enterprise admin settings, security policies, retention policies

- Folders that haven't been explicitly shared with the ITS user

## Why this changed in v4

v3 of this doc asked for Co-Admin on Box because ITS originally targeted JWT / Server Authentication. JWT auth lets a Platform App act as a dedicated service account at the enterprise level — clean ship-and-leave, attribution to "ITS" rather than to a human user, no token expiry.

On 2026-05-20, the JWT path was found to require the paid Box Platform add-on. Standard Box Enterprise does NOT include Custom App authorization in the Admin Console — that's a separate paid feature. Evergreen's Box plan is Enterprise tier but does not include the Box Platform add-on. Co-Admin permissions don't unlock the missing feature because the feature isn't included on the plan, regardless of role.

Procurement of Box Platform was evaluated and declined: the spend is not justified by Customer 0 ITS needs, and a sales conversation under uncertain value-proof conditions is bad timing.

OAuth 2.0 User Authentication is the alternative — it works on standard Enterprise with no add-on, no Custom App authorization, and no admin role beyond ordinary user provisioning. The architectural cost is that ITS attributes its API actions to a real user account rather than a service account. The cost is acceptable for Customer 0 sandbox and initial production; it's mitigated by provisioning a dedicated ITS user (separate from any human's account) so audit trails clearly identify ITS-originated actions.

## What this lets the customer touch (you, post-cutover)

Nothing changes for customer-side users. PMs continue using Box exactly as before. The ITS user account is one additional seat that behaves like any collaborator on the folders it's been added to.

## Ship-and-leave caveat (60-day inactivity window)

OAuth refresh tokens are valid for 60 days from last use. ITS in steady state runs daily workstreams, so the refresh token is exchanged daily and stays valid indefinitely. If ITS goes dark for >60 days (extended outage, indefinitely paused operation, customer unable to run for some reason), the refresh token expires and one operator-touch is required to recover: re-run scripts/setup_box_oauth.py from the cutover MacBook while logged into Box as the ITS user.

Mitigation: a watchdog freshness check (planned for R2 Watchdog Session 2 or later, tracked in docs/tech_debt.md) warns at 50 days idle and CRITICAL at 58 days. Pre-watchdog, the failure mode is loud — the next ITS run after token expiry fails with BoxAuthError, which fires CRITICAL via the triple-fire error_log path. Not silent. Recovery is one terminal command.

In practice: ITS running daily means this caveat never activates. It's documented here so the operator runbook is honest about the one operator-touch condition.

## If you'd rather not provision a dedicated user

ITS can authenticate as your existing operator Box user (e.g., the human admin's own account). Works, but audit trails attribute ITS actions to that human, and any ITS file ownership lands on that human's account. Recommended only if the dedicated-user path has friction (e.g., seat-count licensing concern). Cost: audit-trail clarity.

## Interim path (sandbox → initial production)

Through sandbox and into initial production, ITS authenticates as the operator's sandbox Box user (seths@evergreenmirror.com). At Phase 1.5 cutover, the operator re-runs scripts/setup_box_oauth.py while logged into Box as the new dedicated ITS user; the refresh token in Keychain rotates to the new user; sandbox refresh token revoked from Box account settings. No code change required at migration time. Tracked in docs/tech_debt.md as a Phase 1.5 cutover task.

# Common Ground Across All Three

None of these asks include:

- Billing, payment methods, or financial control of any kind

- Ability to read content (mail, sheets, files) I'm not specifically shared on or that the ITS app/user isn't specifically granted

- Ability to lock you out, remove your admin access, or take over the tenant

- HR, payroll, or PII outside the scope of ITS workstreams

All three systems retain audit logs of admin actions. Anything I do — every app registered, every workspace created, every folder permission changed — is traceable to my account. For Box specifically under v4 OAuth, every ITS API call is traceable to the dedicated ITS user account.

# If You're on the Fence

Reasonable middle path: give me the recommended access in Smartsheet (the workspace topology requires System Admin to provision cleanly). Box requires no admin grant at all under v4 — just a dedicated user account, which is ordinary new-user provisioning. For Microsoft 365, you can start me on the minimum-fallback path; we can revisit M365 after Phase 1 cutover is stable and you've seen ITS run end-to-end in your live tenants.

Box is now the lowest-friction system under v4 — substantially lower than v3 where Co-Admin was needed. Smartsheet remains the most-time-consuming system to fall back on (three-workspace topology × many sheets). M365 is in the middle.

# Authority

Permissions Ask v4, 2026-05-20. Companion to Handover Plan v6.1 (cutover runbook). Supersedes v3 (2026-05-17 evening), which described the Box ask under the now-abandoned JWT / Server Authentication path. v3 retires on acceptance of v4.

# What Changed in v4

- **Box section substantially rewritten. **Co-Admin ask dropped. Replaced with a dedicated standard Box user account (no admin role required) with collaborator access on ITS-relevant folders. Reflects the 2026-05-20 architectural pivot from JWT to OAuth 2.0 User Authentication after discovering JWT requires the Box Platform paid add-on that Evergreen Enterprise does not include.

- **Box Platform add-on procurement explicitly evaluated and declined. **New "Why this changed in v4" subsection captures the architectural reasoning so future operators don't re-litigate the decision. Procurement could be revisited only under specific conditions (ITS value proven + specific OAuth-incompatible requirement emerges).

- **Ship-and-leave caveat added to Box section. **60-day inactivity window explicit. Watchdog freshness check planned (tech_debt entry); pre-watchdog failure mode is loud, not silent.

- **Box fallback path inverted. **In v3, the "if you'd rather keep me below admin" fallback was the harder path (Full Admin does one-time authorization following written instructions). In v4 the primary path IS the lower-friction path; the "if you'd rather not provision a dedicated user" fallback uses the operator's existing user account with the audit-trail-clarity cost.

- **Summary section ****"****Box****"**** line rewritten. **Was "Co-Admin." Now "standard user account (no admin role required)."

- **"****If you****'****re on the fence****"**** section adjusted. **Box is now the lowest-friction system, where in v3 it was middle. Smartsheet remains the most-time-consuming fallback.

- **Cross-references updated. **Handover Plan v5 → v6.1; V&R v6 → v7 (Teams bot reference). M365 + Smartsheet section content unchanged from v3.

- **M365 section unchanged from v3. **Carries forward verbatim including EXO ServicePrincipal note. Handover Plan v3.1 errata pattern remains canonical.

- **Smartsheet section unchanged from v3. **§3.1 three-workspace provisioning + §3.2 customer-side access grants carry forward verbatim. Three-workspace topology unchanged.