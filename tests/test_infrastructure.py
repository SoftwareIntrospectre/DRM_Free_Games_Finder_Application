import unittest
from aws_infrastructure.cloudwatch.cloudwatch_config import CloudWatchMonitor
from aws_infrastructure.terraform.main import TerraformProvisioner

class TestInfrastructure(unittest.TestCase):

    def test_cloudwatch_config(self):
        monitor = CloudWatchMonitor()
        success = monitor.configure()
        self.assertTrue(success)  # Assuming configure returns True if configuration succeeds

    def test_terraform_provisioning(self):
        provisioner = TerraformProvisioner()
        result = provisioner.apply_changes()
        self.assertTrue(result)  # Assuming apply_changes returns True if successful

if __name__ == "__main__":
    unittest.main()
