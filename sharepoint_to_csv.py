import os
from shareplum import Site
from requests_ntlm import HttpNtlmAuth
import pandas as pd
import requests

def sharepoint_to_csv(
    website_root    = '<Sharepoint URL>'
    ,list_id        = '{974e11d3-c26c-4dfe-83d6-317ef2cda73f}'
    ,list_view      ='All fields'
    ,calculated_fields = ['Alert Status','Send Month']
    ,user_id        = "corpau\\"+os.environ["UNAME"]
    ,user_pwd       = os.environ['PWD']
    ,output_csv_path = '~/data/sharepoint/'+'progress_letter_hist.csv'
):
    '''
    Extract a table from a sharepoint view of a list and output to a csv
    
    params
        website_root: base url for the sharepoint site of interest
        list_id: Unqiue 'list' identifier, this can be found by going to the table of interest
                 clicking on the 'LIST' tab, then on the 'List Settings' button in the ribbon.
                 The url should have an id that looks like: List=%7B974E11D3-C26C-4DFE-83D6-317EF2CDA73F%7D
                 To convert this to a list id, replace '%7B' with '{' and '%7D' with '}'
                 The unique list id will be: {974e11d3-c26c-4dfe-83d6-317ef2cda73f}
        list_view: The name of the view of the list you want to download, found above the list/data when viewing it
        calculated_fields: Calculated fields have a bug in the sharepoint API where they extract 
                            with a prefix string#;, columns listed here will have this removed.
        user_id: staff id, best store this as an environment variable, os.environ["UNAME"] 
        user_pwd: lan password, best store this as an environment variable, os.environ['PWD']
        output_csv_path: the output path for the .csv to be generated, e.g. 'c:/data/sharepoint/extract.csv'

    notes
        Had an issue with invalid XML characters which appears to be ironed out in a more recent verison. 
        Fixed it locally by adding ',recover=True' to the XML parser object in shareplum for now, need to update later.
        https://github.com/jasonrollins/shareplum/issues/36
    '''
    # Connect to the Sharepoint with Progress Letter Data
    requests.packages.urllib3.disable_warnings() #suppress missing ssl warnings
    auth = HttpNtlmAuth(user_id, user_pwd)
    site = Site(website_root, auth=auth,verify_ssl=False)
    sp_list = site.List(list_id)
    data = sp_list.GetListItems(list_view)

    # Convert to a pandas dataframe
    data_df = pd.DataFrame(data)

    # Clean up a sharepoint bug where calculated fields prefix their value with string;#
    # https://sympmarc.com/2008/08/13/string-before-values-in-a-sharepoint-lists-lookup-column-based-on-a-calculated-value/
    # Hotfix available but may not work
    for field in calculated_fields:
        data_df[field] = data_df[field].str.replace('string;#','')

    # Output csv to be uploaded to teradata
    data_df.to_csv(output_csv_path,index=False)

