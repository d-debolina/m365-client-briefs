#!/usr/bin/env bash
# CARGO: storage account for Power Pages attachments (Azure CLI). Review names/region before running.
set -euo pipefail
RG=rg-cargo-demo; LOC=westeurope; SA=stcargodemo$RANDOM; CONTAINER=pp-attachments
SITE_APP="Portals-contoso-claims"      # the Power Pages site's Entra app: Portals-<site name>

az group create -n $RG -l $LOC
az storage account create -n $SA -g $RG -l $LOC --sku Standard_LRS --kind StorageV2 \
  --min-tls-version TLS1_2 --allow-blob-public-access false
az storage container create --account-name $SA -n $CONTAINER --auth-mode login --public-access off

# RBAC for the site's app (as documented): Reader on the resource group + Storage Blob Data Contributor on the account
APP_ID=$(az ad sp list --display-name "$SITE_APP" --query "[0].id" -o tsv)
az role assignment create --assignee-object-id $APP_ID --assignee-principal-type ServicePrincipal --role Reader --scope $(az group show -n $RG --query id -o tsv)
az role assignment create --assignee-object-id $APP_ID --assignee-principal-type ServicePrincipal --role "Storage Blob Data Contributor" --scope $(az storage account show -n $SA -g $RG --query id -o tsv)

# CORS so the model-driven app web resource can preview/download (tighten origins in production)
az storage cors add --services b --account-name $SA --methods GET PUT OPTIONS --origins "https://contoso.crm.dynamics.com" \
  --allowed-headers "*" --exposed-headers "*" --max-age 200

# Lifecycle: move attachments to Cool after 30 days, Archive after 365 (cheaper long-term storage)
cat > lifecycle.json <<'JSON'
{"rules":[{"enabled":true,"name":"age-out","type":"Lifecycle","definition":{"filters":{"blobTypes":["blockBlob"],"prefixMatch":["pp-attachments/"]},
 "actions":{"baseBlob":{"tierToCool":{"daysAfterModificationGreaterThan":30},"tierToArchive":{"daysAfterModificationGreaterThan":365}}}}}]}
JSON
az storage account management-policy create --account-name $SA -g $RG --policy @lifecycle.json
echo "Storage account: $SA  container: $CONTAINER"
