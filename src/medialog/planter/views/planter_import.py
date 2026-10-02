# -*- coding: utf-8 -*-

# from medialog.planter import _
# -*- coding: utf-8 -*-
# import csv
import io
import requests
# from plone import api
from Products.CMFPlone.utils import getSite
from Products.Five import BrowserView
from zope.interface import Interface
#from zope.schema import Bytes
from z3c.form import form, field, button
from plone.namedfile.field import NamedBlobFile 
from zope.annotation.interfaces import IAnnotations
from persistent.list import PersistentList

from Products.CMFPlone.utils import getSite
from io import BytesIO
import pandas as pd
from plone import api 


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IPlanterImport(Interface):
    """ Marker Interface for IPlanterImport"""

 
class IPlanterImportFormSchema(Interface):
    
    excel_file = NamedBlobFile(
        title=u"Excel File",
        description=u"Last opp plantefil",
        required=False
    )
 

class PlanterImport(form.Form):
    fields = field.Fields(IPlanterImportFormSchema)
    ignoreContext = True
    label = u"Import planteliste fra Excel"

    @button.buttonAndHandler(u"Import")
    def handleImport(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        file_data = data['excel_file']

        # Get raw bytes from the upload
        if hasattr(file_data, 'data'):                 # plone.namedfile NamedBlobFile
            raw = file_data.data
        elif hasattr(file_data, 'read'):               # ZPublisher FileUpload
            raw = file_data.read()
        elif isinstance(file_data, (bytes, bytearray)):
            raw = bytes(file_data)
        else:
            self.status += f"Wrong or missing Excel file"
            return None
            # raise ValueError("Unsupported upload type for Excel file")
        

        # Read the sheet as strings for the rest of the data
        df = pd.read_excel(BytesIO(raw), sheet_name=0, dtype=str)
        df = df.fillna("")
        df.columns = [str(c).strip().lower() for c in df.columns]
        rows = df.to_dict(orient="records")

        portal = api.portal.get()

        # import pdb; pdb.set_trace()
 
        for row_idx, row in enumerate(rows):

            # Use the Excel "title" column as the Plone title
            title = row.get("title", "")

            # Remove title so it isn't passed twice
            data = row.copy()
            data.pop("title", None)

            plante = api.content.create(
                type="plante",
                container=portal,
                title=title,
                **data
            )
