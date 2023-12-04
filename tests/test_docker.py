import unittest

from docker import from_env


class TestDockerfile(unittest.TestCase):
    def setUp(self):
        print("Setting up the test...")
        self.client = from_env()
        print("Building the image...")
        self.image, _ = self.client.images.build(path=".", tag="myapp:test")
        print("Docker image built.")

    def test_image_build(self):
        print("Testing image build...")
        self.assertIsNotNone(self.image)
        print("Image build test passed.")

    def test_container_run(self):
        print("Testing container run...")
        container = self.client.containers.run("myapp:test", detach=True)
        self.assertTrue(container.status == "running")
        print("Container run test passed.")
        container.stop()

if __name__ == "__main__":
    unittest.main()
