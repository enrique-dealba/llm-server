import unittest
from docker import from_env

class TestDockerfile(unittest.TestCase):
    def setUp(self):
        self.client = from_env()
        self.image, _ = self.client.images.build(path=".", tag="myapp:test")

    def test_image_build(self):
        self.assertIsNotNone(self.image)

    def test_container_run(self):
        container = self.client.containers.run("myapp:test", detach=True)
        self.assertTrue(container.status == "running")
        container.stop()

if __name__ == "__main__":
    unittest.main()
