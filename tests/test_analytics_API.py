# ----------------------------------------------------------------------------------------------------------------------
#    Analytics API tests
# ----------------------------------------------------------------------------------------------------------------------

# imports
import unittest
import tempfile
import os
import shutil
import logging

import analytics_API as Api


class TestAnalyticsApi(unittest.TestCase):
    """
    Test functions for the Analytics API functions.
    """
    def setUp(self):
        """
        Initialize test specific variables.
        """
        self.logger = logging.getLogger(__name__)
        self.logs_dir = tempfile.mkdtemp()

    def tearDown(self):
        """
        Performs any necessary clean up.
        """
        if os.path.exists(self.logs_dir):
            shutil.rmtree(self.logs_dir)

    def test_nominal(self):
        """

        """
        self.assertTrue(True)

    def test_nominal_2(self):
        """

        """
        self.assertTrue(True)


# ----------------------------------------------------------------------------------------------------------------------
#    End
# ----------------------------------------------------------------------------------------------------------------------
