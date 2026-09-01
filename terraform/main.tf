// A short random suffix, generated once and then held in state.
//
// The container registry name has to be unique across every Azure customer on
// earth, so "ecomapiacr" is almost certainly taken. This makes the name unique
// without making it unpredictable: `keepers` is empty, so the suffix is stable
// across applies and only changes if the whole stack is destroyed and rebuilt.
resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

// One resource group holds everything.
//
// This is the single most useful safety property of the whole stack: deleting
// this group deletes every resource inside it. `terraform destroy` is the
// correct way to tear down, but the group is the backstop that guarantees
// nothing is left quietly billing after the demo is over.
resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-rg"
  location = var.location

  tags = local.tags
}

locals {
  suffix = random_string.suffix.result

  // Tags are not decoration. `expires` is a note to your future self, and
  // `cost-center` is the field a real employer filters the bill by.
  tags = {
    project     = "enterprise-ecommerce-api"
    managed-by  = "terraform"
    environment = "demo"
    owner       = "seyi-oladejo"
  }
}
