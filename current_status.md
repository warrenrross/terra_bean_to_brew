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

> Hi Professor, I'm now on the Azure for Students subscription (03d4bee9-df57-4c11-8c04-62b0be1dd604) with the Contributor role. Thank you.
>
> My Terraform deploy created the resource group, Log Analytics, Application Insights, and storage account in northcentralus (the region policy allows only francecentral, denmarkeast, mexicocentral, belgiumcentral, and northcentralus). It fails when creating the App Service plan: both F1 and B1 show a quota of 0 in northcentralus ("Operation cannot be completed without additional quota... Current Limit (F1 VMs): 0"). I tried requesting an increase with `az quota create`, but it returns `ResourceNotAvailableForOffer`, so the Students offer doesn't allow self-service increases.
>
> Could you either raise the App Service quota (F1 and B1) for this subscription, or let me know which region/SKU has quota available for the class? Otherwise I can host the static site on the storage account's static website feature instead of App Service. Let me know which you prefer.
>
> Thanks, Warren
