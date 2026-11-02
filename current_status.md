# Current Status — terra_bean_to_brew

_Last updated: 2026-11-02_

## Summary

Dev deployment is **partially applied**. 4 of 6 resources exist in `rg-beantobrew-dev`. The App Service plan and web app are blocked because the subscription has **0 App Service quota** (F1 and B1) in `northcentralus`, and Azure for Students will not let us raise it.

## Environment

| Item | Value |
|------|-------|
| Subscription | Azure for Students (`03d4bee9-df57-4c11-8c04-62b0be1dd604`) |
| Account | `wr022@uark.edu` (Contributor) |
| Region | `northcentralus` |
| Workspace | `dev` |
| Env vars | `ARM_SUBSCRIPTION_ID=03d4bee9-df57-4c11-8c04-62b0be1dd604`, `ARM_RESOURCE_PROVIDER_REGISTRATIONS=none` |

## What Worked

- Signed in to the new subscription after an `az account list --refresh`. Reads and writes work (Contributor).
- Found the region policy ("Allowed resource deployment regions"): only `francecentral`, `denmarkeast`, `mexicocentral`, `belgiumcentral`, `northcentralus` are allowed. Changed `location` in `environments/dev.tfvars` and `environments/prod.tfvars` from `centralus` to `northcentralus`.
- `terraform plan -var-file=environments/dev.tfvars` succeeded (6 to add).
- `terraform apply` created these in `rg-beantobrew-dev`:
  - Resource group `rg-beantobrew-dev`
  - Log Analytics workspace `law-beantobrew-dev`
  - Application Insights `appi-beantobrew-dev`
  - Storage account `stbeantobrewdevby15e`
- Registered `Microsoft.Quota` on the subscription so the quota API could be queried.

## What Didn't Work

| Attempt | Result |
|---------|--------|
| Apply with F1 (free) plan | 401 `Operation cannot be completed without additional quota`. Current limit (F1 VMs): 0 |
| Apply with B1 plan (then reverted to F1) | Same error. Current limit (B1 VMs): 0 |
| `az quota create` for F1 = 1 in `northcentralus` | `ResourceNotAvailableForOffer`. The Students offer can't raise App Service quota |
| `az quota list` for francecentral, denmarkeast, mexicocentral, belgiumcentral | Returns only a wildcard entry (`isQuotaApplicable: false`), so real quota can't be read |
| Scratch plan probes: F1 and B1 in each of those 4 regions | All 8 failed: `App Service Plan Create operation is throttled for subscription ... Please contact support if issue persists`. Inconclusive; likely triggered by our repeated failed attempts. Scratch RG deleted |
| Earlier subscription (UITS-VDI) | 403 on `resourceGroups/read`. No rights. Superseded by the new subscription |

Not yet tried: the other four allowed regions (quota may differ), or Azure Storage static website hosting (no App Service quota needed).

## Not Done Yet

- App Service plan `asp-beantobrew-dev` and web app `app-beantobrew-dev-by15e`
- Bean to Brew site files not deployed
- Prod environment not started

## Next Steps

1. Send the message below to the instructor.
2. Optionally probe `francecentral`, `denmarkeast`, `mexicocentral`, `belgiumcentral` for F1/B1 quota. Changing region recreates the 4 empty resources.
3. Fallback: host the static site on the storage account's static website feature.
4. Once quota exists: `terraform apply -var-file=environments/dev.tfvars`, deploy the site, then promote to prod.

## Message to Instructor:

> **Subject:** Azure for Students sub 03d4bee9: App Service plan blocked (quota 0 / throttled), need help
>
> Hi Professor [Name],
>
> Thank you for the subscription. I'm signed in as wr022@uark.edu with the Contributor role on **Azure for Students (03d4bee9-df57-4c11-8c04-62b0be1dd604)**. My Terraform repo is at https://github.com/warrenrross/terra_bean_to_brew, and the full history of what I tried is in the commit log and `current_status.md`.
>
> **What worked:** `terraform plan` succeeds (6 to add). `terraform apply` for dev created 4 of 6 resources in `rg-beantobrew-dev` (resource group, Log Analytics, Application Insights, storage account) in `northcentralus`. I picked that region because the "Allowed resource deployment regions" policy on my subscription allows only francecentral, denmarkeast, mexicocentral, belgiumcentral and northcentralus.
>
> **What fails:** creating the App Service plan (`asp-beantobrew-dev`), so the web app can't be created either:
> - F1 (dev): `401 Unauthorized: Operation cannot be completed without additional quota. Current Limit (F1 VMs): 0 ... (Minimum) New Limit that you should request to enable this deployment: 1`
> - B1 (prod SKU, tried as a test): same error, `Current Limit (B1 VMs): 0`
> - Requesting an increase myself with `az quota create` (F1 = 1, northcentralus) returns `ResourceNotAvailableForOffer`, so the Students offer doesn't allow self-service increases.
> - I then tried to test the other four allowed regions with scratch App Service plans (F1 and B1 in each). All eight attempts returned `App Service Plan Create operation is throttled for subscription 03d4bee9-... Please contact support if issue persists`, so I couldn't find out whether those regions have quota. The throttle is probably from my repeated failed attempts. I stopped to avoid making it worse.
>
> **Questions:**
> 1. Can you raise the App Service quota (F1 for dev, B1 for prod) on this subscription, or tell me which allowed region and SKU should have quota?
> 2. Is the throttle something that clears on its own, and about how long should I wait before retrying?
> 3. If App Service isn't possible on this subscription, would hosting the Bean to Brew static site on the storage account's static website feature (no App Service quota needed) be acceptable for this assignment?
>
> I'm happy to try a specific region if you tell me which one. Thanks for your help.
>
> Warren Ross

## Details to attach or paste if asked

| Item | Value |
|------|-------|
| Subscription | Azure for Students, `03d4bee9-df57-4c11-8c04-62b0be1dd604` |
| Account / role | `wr022@uark.edu`, Contributor |
| Region used | `northcentralus` |
| Resources created | `rg-beantobrew-dev`, `law-beantobrew-dev`, `appi-beantobrew-dev`, `stbeantobrewdevby15e` |
| Resources blocked | `asp-beantobrew-dev` (App Service plan), `app-beantobrew-dev-by15e` (web app) |
| Terraform | `terraform apply -var-file=environments/dev.tfvars`, workspace `dev`, azurerm provider |
| Repo | https://github.com/warrenrross/terra_bean_to_brew |
