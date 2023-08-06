from mitosheet_helper_config.mito_config_utils import *

"""
This file contains all of the Mito configuration options for Enterprise admins.

To configure your Mito deployment, follow the instructions above each of the entries
in the MITO_ENTERPRISE_CONFIGURATION dictionary below.
"""

MITO_ENTERPRISE_CONFIGURATION = {
	# The MEC_VERSION is used internally by Mito to properly read the 
	# MITO_ENTERPRISE_CONFIGURATION dictionary. Do not edit.
	MEC_VERSION: 1,

	# Users get directed to the SUPPORT_EMAIL when an error occurs or they seek help. 
	# Update the SUPPORT_EMAIL with a valid email address. If the SUPPORT_EMAIL is None, 
	# users will get directed to the Mito community slack. The final result should look like:
	# 	
	# 	SUPPORT_EMAIL: 'mito_support@company.com',
	SUPPORT_EMAIL: None, 
}