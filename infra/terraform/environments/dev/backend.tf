terraform {
  backend "s3" {
    bucket         = "rwa-control-tower-tfstate-dev"
    key            = "dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "rwa-control-tower-tfstate-lock"
    encrypt        = true
  }
}
