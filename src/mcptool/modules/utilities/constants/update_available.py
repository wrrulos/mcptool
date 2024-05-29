from ..update.update_utilities import UpdateUtilities
from . import VERSION, GITHUB_REPOSITORY

# Check if an update is available
UPDATE_AVAILABLE: bool = UpdateUtilities.update_available(VERSION, GITHUB_REPOSITORY)
