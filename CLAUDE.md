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
| `location = northcentralus` in both tfvars | Subscription policy allows only francecentral, denmarkeast, mexicocentral, belgiumcentral, northcentralus; closest to Arkansas. User chose to stay here for now |
| Dev SKU stays F1 | Guide convention; B1 was tried and also has 0 quota, so reverted |

## Known Issues
| Issue | Status | Notes |
|-------|--------|-------|
| App Service plan fails: 401 "additional quota", F1 and B1 limit = 0 in `northcentralus` | OPEN | `az quota create` returns `ResourceNotAvailableForOffer` (Students offer can't self-raise). Message to instructor drafted in `current_status.md` |
| Dev partially applied | OPEN | 4 of 6 resources exist in `rg-beantobrew-dev` (RG, Log Analytics, App Insights, storage `stbeantobrewdevby15e`). Plan + web app missing; state matches Azure |
| App code not deployed | OPEN | Needs web app (or storage static-website fallback) first |
| Old UITS-VDI subscription 403 | RESOLVED | Superseded by the Azure for Students subscription |

## Pending Tasks
1. Send the instructor message in `current_status.md`; wait for quota or a region/SKU that has it
2. Optional meanwhile: probe the other allowed regions for F1/B1 quota (region change recreates the 4 empty resources); fallback is storage static-website hosting
3. Once quota exists: `terraform apply` for dev, deploy Bean to Brew files, promote to prod, tear down when done

## Session History
| Date | Work Done |
|------|-----------|
| 2026-10-21 | Scaffolded repo from guide, pushed to github.com/warrenrross/terra_bean_to_brew, moved to Cloud Computing dir, installed az + terraform, signed in, dev plan OK (7 to add), apply blocked by 403 |
| 2026-11-02 | Switched to instructor's Azure for Students sub, set region to northcentralus (policy), partial dev apply (4/6), blocked by 0 F1/B1 quota, quota request rejected by offer, wrote `current_status.md` with instructor message |
