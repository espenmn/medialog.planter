# -*- coding: utf-8 -*-
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)

import medialog.planter


class MedialogPlanterLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=medialog.planter)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'medialog.planter:default')


MEDIALOG_PLANTER_FIXTURE = MedialogPlanterLayer()


MEDIALOG_PLANTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEDIALOG_PLANTER_FIXTURE,),
    name='MedialogPlanterLayer:IntegrationTesting',
)


MEDIALOG_PLANTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MEDIALOG_PLANTER_FIXTURE,),
    name='MedialogPlanterLayer:FunctionalTesting',
)
