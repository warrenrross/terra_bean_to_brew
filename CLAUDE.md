# CLAUDE.md — terra_bean_to_brew

## What This Project Is
Terraform that deploys the Bean to Brew static site (https://github.com/warrenrross/Bean_to_Brew) to Azure with dev and prod environments. Follows https://github.com/shellywaltersit/platform/blob/main/docs/terraform-azure-webapp-guide.md. Coursework for DASC Cloud Computing.

## Session-Start Checklist
1. Read this file and `current_status.md` (what worked / didn't, plus the drafted instructor message)
2. Check `az account show` (should be `Azure for Students`, `03d4bee9-…`; `az login` / `az account list --refresh` if not)
3. Check whether the instructor has replied about App Service quota (see Known Issues)

## Key Workflows
```bash
export ARM_SUBSCRIPTION_ID=03d4bee9-df57-4c11-8c04-62b0be1dd604   # Azure for Students (instructor-provided, Contributor)
export ARM_RESOURCE_PROVIDER_REGISTRATIONS=none                   # keep: avoids provider auto-registration attempts
terraform workspace select dev            # workspace must match the tfvars file
terraform plan  -var-file=environments/dev.tfvars
terraform apply -var-file=environments/dev.tfvars
```

## Architecture Decisions
| Decision | Rationale |
|----------|-----------|
| `project` default is `beantobrew` (not `webapp`) | User wanted resources named for the app; 10 chars is the validation max |
| Guide template kept as written (Node 22 Linux web app) | Convention required; app is static HTML/JS, so serving it needs a small Node server or a stack change |
| Provider auto-registration disabled via env var, not code | Keeps code identical to template |
| Repo lives in `~/Education/DASC/Cloud Computing/` | User asked to move it there |
| `location = denmarkeast` in both tfvars | Policy allows only francecentral, denmarkeast, mexicocentral, belgiumcentral, northcentralus. Probe 2026-11-06: denmarkeast + belgiumcentral have F1/B1 quota, northcentralus has 0, francecentral/mexicocentral throttled (unknown) |
| Resource group stays `rg-beantobrew-<env>` | A `wross` owner prefix was tried (6893f60) then reverted (0b08ced) to keep the already-working dev group. Subscription is shared with other students, but `beantobrew` is specific to this project (clashes seen were from generic names), so no owner prefix is needed, including for prod |
| App served by a small `server.js` added at deploy time | Bean_to_Brew is pure static; zip (index.html, css, js, data, pages, assets + server.js + package.json; first deploy omitted pages/ and assets/ so nav links 404'd, fixed) is built outside the app repo and pushed with `az webapp deploy --type zip` |
| Dev SKU stays F1 | Guide convention; F1 works in denmarkeast |

## Known Issues
| Issue | Status | Notes |
|-------|--------|-------|
| App Service quota 0 in `northcentralus` | RESOLVED | Moved to `denmarkeast`, where F1 works |
| Azure PIM: Contributor must be activated | WATCH | Role is eligible, not permanent. `AuthorizationFailed` on everything = activate in portal (PIM > My roles > Azure resources), then `az logout && az login` |
| Flaky 404s on reads in denmarkeast | WATCH | Terraform plan/import intermittently reports resources "deleted" or 404s. Retry; confirm with `az resource list` before applying |
| Dev web app imported into state; pending in-place change | OPEN | `terraform apply` will set the App Insights connection string app setting (harmless). Run it, then plan should be empty |
| App Insights Smart Detection action group | WATCH | Auto-created, not in Terraform, stalled a resource group delete once; `az monitor action-group delete` unblocked it |
| Prod environment | DONE | Applied 7/7 in `denmarkeast` (B1, workspace `prod`), site deployed: https://app-beantobrew-prod-2i3bb.azurewebsites.net |

## Pending Tasks
1. `terraform apply -var-file=environments/dev.tfvars -auto-approve` (run by the user; Claude's auto mode blocks it) to clear the one pending change
2. Tear down dev and prod when the course is done (`terraform workspace select <env>` then `terraform destroy -var-file=environments/<env>.tfvars`); prod B1 is paid

## Session History
| Date | Work Done |
|------|-----------|
| 2026-10-21 | Scaffolded repo from guide, pushed to github.com/warrenrross/terra_bean_to_brew, moved to Cloud Computing dir, installed az + terraform, signed in, dev plan OK (7 to add), apply blocked by 403 |
| 2026-11-02 | Switched to instructor's Azure for Students sub, set region to northcentralus (policy), partial dev apply (4/6), blocked by 0 F1/B1 quota, quota request rejected by offer, wrote `current_status.md` with instructor message |
| 2026-11-06 | Role was PIM-eligible (reactivated, re-logged in), probed all 5 regions, moved to denmarkeast, dev applied (state repaired by import + untaint after connection reset), tried and reverted wross RG prefix, deployed Bean to Brew: https://app-beantobrew-dev-by15e.azurewebsites.net |
| 2026-11-06 (later) | Applied prod (7 resources), deployed same zip, both sites return 200 with Bean to Brew content |
