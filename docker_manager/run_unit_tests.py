#!/usr/bin/env python3

import unittest
# Import your test classes
from test_docker_config import TestDockerConfig
from test_docker_container_manager import TestDockerContainerManager
from test_docker_dependency_checker import TestDockerDependencyChecker
from test_docker_image_builder import TestDockerImageBuilder
from test_docker_service_manager import TestDockerServiceManager
from test_docker_utility import TestDockerUtility


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDockerConfig))
    suite.addTest(unittest.makeSuite(TestDockerContainerManager))
    suite.addTest(unittest.makeSuite(TestDockerDependencyChecker))
    suite.addTest(unittest.makeSuite(TestDockerImageBuilder))
    suite.addTest(unittest.makeSuite(TestDockerServiceManager))
    suite.addTest(unittest.makeSuite(TestDockerUtility))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
