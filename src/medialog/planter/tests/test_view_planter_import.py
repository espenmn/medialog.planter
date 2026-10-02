# -*- coding: utf-8 -*-
from medialog.planter.testing import MEDIALOG_PLANTER_FUNCTIONAL_TESTING
from medialog.planter.testing import MEDIALOG_PLANTER_INTEGRATION_TESTING
from medialog.planter.views.planter_import import IPlanterImport
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_PLANTER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_planter_import_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='planter-import'
        )
        self.assertTrue(IPlanterImport.providedBy(view))

    def test_planter_import_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='planter-import'
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = IPlanterImport.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = MEDIALOG_PLANTER_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
