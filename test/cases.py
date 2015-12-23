from google.appengine.datastore.datastore_stub_util import PseudoRandomHRConsistencyPolicy

import unittest
from app.league.models import create_league
from app.participant.models import create_participant
from app.user.models import create_user
import main
import mock
from google.appengine.ext import testbed
import os


class BaseGAETestCase(unittest.TestCase):
    APP_ROOT_PATH = os.path.join(os.path.dirname(__file__), '../../../src')

    def mock_function_in_setup(self, path, **kwargs):
        """
        Used in a TestCase's setUp method to patch a function with a Mock instance. Returns the Mock object.
        """
        patcher = mock.patch(path, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def setUp(self):
        """
        Set up the GAE test environment
        """
        # Create and activate testbed
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # Declare which service stubs to use - these stubs provide test functionality that does not require ues of
        # the real GAE services under test. E.g., using the datastore stub will test against an in-memory datastore.
        # See https://developers.google.com/appengine/docs/python/tools/localunittesting
        self.testbed.init_taskqueue_stub(_all_queues_valid=True, root_path=self.APP_ROOT_PATH)
        self.testbed.init_app_identity_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_capability_stub()
        self.testbed.init_files_stub()
        self.testbed.init_blobstore_stub()
        self.testbed.init_search_stub()
        self.testbed.init_user_stub()
        # Urlfetch stub
        # =============

        self.mock_function_in_setup('urllib2.urlopen',
                                    side_effect=ValueError('urllib2 urlopen is not allowed in unit tests'))
        self.mock_function_in_setup('httplib.HTTPConnection.request',
                                    side_effect=ValueError('HTTPConnection request is not allowed in unit tests'))
        # Datastore stub
        # ==============
        policy = PseudoRandomHRConsistencyPolicy(probability=1)

        self.testbed.init_datastore_v3_stub(consistency_policy=policy,
                                            require_indexes=True,
                                            root_path=self.APP_ROOT_PATH)

    def tearDown(self):
        """
        Tear down the GAE test environment
        """
        self.testbed.deactivate()

    # Stub getters
    # ============
    def get_taskqueue_stub(self):
        """ Get the taskqueue stub """
        taskqueue_stub = self.testbed.get_stub('taskqueue')
        if taskqueue_stub:
            return taskqueue_stub
        else:
            raise ValueError('Taskqueue stub not initialized.')

    def get_app_identity_stub(self):
        """ Get the app identity stub """
        app_identity_stub = self.testbed.get_stub('app_identity_service')
        if app_identity_stub:
            return app_identity_stub
        else:
            raise ValueError('App identity stub not initialized.')

    def get_memcache_stub(self):
        """ Get the memcache stub """
        memcache_stub = self.testbed.get_stub('memcache')
        if memcache_stub:
            return memcache_stub
        else:
            raise ValueError('Memcache stub not initialized.')

    def get_capability_stub(self):
        """ Get the capablity stub """
        capability_stub = self.testbed.get_stub('capability_service')
        if capability_stub:
            return capability_stub
        else:
            return ValueError('Capability stub not initialized.')

    def get_files_stub(self):
        """ Get the files stub """
        files_stub = self.testbed.get_stub('file')
        if files_stub:
            return files_stub
        else:
            raise ValueError('Files stub not initialized.')

    def get_blobstore_stub(self):
        """ Get the blobstore stub """
        blobstore_stub = self.testbed.get_stub('blobstore')
        if blobstore_stub:
            return blobstore_stub
        else:
            raise ValueError('Blobstore stub not initialized.')

    def get_search_stub(self):
        """ Get the search stub """
        search_stub = self.testbed.get_stub('search')
        if search_stub:
            return search_stub
        else:
            raise ValueError('Search stub not initialized.')

    def get_urlfetch_stub(self):
        """ Get the urlfetch stub """
        urlfetch_stub = self.testbed.get_stub('urlfetch')
        if urlfetch_stub:
            return urlfetch_stub
        else:
            raise ValueError('Urlfetch stub not initialized.')

    def get_datastore_stub(self):
        """ Get the datastore stub """
        datastore_stub = self.testbed.get_stub('datastore_v3')
        if datastore_stub:
            return datastore_stub
        else:
            raise ValueError('Datastore stub not initialized.')

    def get_user_stub(self):
        """ Get the datastore stub """
        user_stub = self.testbed.get_stub('user')
        if user_stub:
            return user_stub
        else:
            raise ValueError('User stub not initialized.')


class BaseFlaskTestCase(BaseGAETestCase):
    def create_test_user(self):
        self.user = create_user('nepnep', name='Neptune', company_name='Planeptune')

    def create_test_league(self):
        self.create_test_user()
        self.league = create_league(self.user, name="Nep League", rating_scheme='ELO',
                                    k_sensitivity='Low', k_factor_scaling=10)

    def create_test_participant(self):
        self.create_test_user()
        self.create_test_league()
        self.participant = create_participant(self.user, self.league.league_id, 'Nepgear')

    def setUp(self):
        super(BaseFlaskTestCase, self).setUp()
        self.app = main.app.test_client()
        self.user = None
        self.league = None
        self.participant = None