# terra_bean_to_brew

Terraform that deploys the [Bean to Brew](https://github.com/warrenrross/Bean_to_Brew) web app to Azure, with separate **dev** and **prod** environments built from the same code. It follows the convention in the
[Terraform on Azure guide](https://github.com/shellywaltersit/platform/blob/main/docs/terraform-azure-webapp-guide.md).

Resources are named `<abbreviation>-beantobrew-<environment>` (for example `rg-beantobrew-dev`, `app-beantobrew-dev-k3x9p`).

## Layout

```text
├── providers.tf            azurerm + random providers
├── variables.tf            inputs (project defaults to "beantobrew")
├── main.tf                 resource group, Log Analytics, App Insights, App Service plan + web app, storage, optional SQL/Postgres
├── outputs.tf              web app name/URL, storage account, DB hostnames
└── environments/
    ├── dev.tfvars          F1 (free) plan
    └── prod.tfvars         B1 plan
```

## Check locally (no Azure sign-in needed)

```bash
terraform init
terraform fmt
terraform validate
```

## Deploy

Workspace and `.tfvars` file must match (the plan fails otherwise).

```bash
export ARM_SUBSCRIPTION_ID=<your-subscription-id>

terraform workspace new dev          # first time only; later: terraform workspace select dev
terraform plan  -var-file=environments/dev.tfvars
terraform apply -var-file=environments/dev.tfvars

terraform workspace new prod         # promote once dev is verified
terraform plan  -var-file=environments/prod.tfvars
terraform apply -var-file=environments/prod.tfvars
```

Update `location` in the `.tfvars` files to a region your subscription allows. See the
companion guide "Azure for Students: Deploying with the CLI" for sign-in and region lookup.

## Deploying the app code

Bean to Brew is a static HTML/CSS/JS site. The web app created here is a Linux App Service running a Node 22 stack (per the guide's template), so deploy the site's files and serve them with a small Node static server, or change the stack in `main.tf` if you prefer another approach. Packaged code (`app.zip`) is git-ignored.

## Teardown

```bash
terraform destroy -var-file=environments/<env>.tfvars
```
