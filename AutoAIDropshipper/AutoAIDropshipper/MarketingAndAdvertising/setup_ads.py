from facebook_business.api import FacebookAdsApi

my_app_id = '<app-id>'
my_app_secret = '<app-secret>'
my_access_token = '<access-token>'

FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign

# Define the ad account ID
ad_account_id = '<ad-account-id>'

# Define the campaign parameters
campaign = Campaign(parent_id=ad_account_id)
campaign.update({
    Campaign.Field.name: 'My Campaign',
    Campaign.Field.objective: 'LINK_CLICKS',
})

# Create the campaign
campaign.remote_create(params={
    'status': Campaign.Status.paused,
})

# Print the campaign ID
print(campaign[Campaign.Field.id])