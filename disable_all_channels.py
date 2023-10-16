import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv('SERVER_URL')
API_KEY = os.getenv('API_KEY')
CHANNEL_EXCLUSION_SEARCH_TERMS = str(os.getenv('CHANNEL_EXCLUSION_SEARCH_TERMS')).split(',')

channel_loop_index = 0

# Get all channels
get_channels_query = {
  'SortBy':'DefaultChannelOrder', 
  'SortOrder':'Descending',
  'Fields':'BasicSyncInfo%2CCanDelete%2CContainer%2CPrimaryImageAspectRatio%2CProductionYear%2CStatus%2CEndDate%2CCommunityRating%2COfficialRating%2CCriticRating',
  'StartIndex':channel_loop_index,
  'EnableImageTypes':'Primary%2CBackdrop%2CThumb',
  'ImageTypeLimit':'1',
  'Limit':'30',
  'X-Emby-Token':API_KEY,
  'X-Emby-Language':'en-us',
  }

get_channels_response = requests.get(SERVER_URL + "/emby/LiveTv/Manage/Channels", params=get_channels_query)

channels = get_channels_response.json()

# Example of Single Channel's Data:
# {'Name': 'US| MAGNOLIA CHANNEL HD', 
#  'ServerId': 'fe12a368204e41348dc76fbcf9baf2a8', 
#  'Id': '699973', 
#  'SortIndexNumber': 25, 
#  'ChannelNumber': '254715', 
#  'Type': 'ChannelManagementInfo', 
#  'ImageTags': {'Primary': '6a1e338c9f7458bf3ac44712085a376a'}, 
#  'BackdropImageTags': [], 
#  'Disabled': False, 
#  'ManagementId': '4ab97cfd1764498fb930c78539b9fb29_m3u_72d5a993df2923b222644d4ad055215b81659f8e21582271b85b15899614e094'
#  }

i = 0
# Now that we have the initial count of channels, start the loop
while len(channels['Items']) > 0:

  # Disable channels
  for channel in channels['Items']:
      i += 1
      name = channel['Name']
      id = channel['Id']
      management_id = channel['ManagementId']
      disabled = channel['Disabled']
      exclusion_term_detected = False
      for term in CHANNEL_EXCLUSION_SEARCH_TERMS:
          if term.lower() in name.lower():
              exclusion_term_detected = True
      if not disabled and not exclusion_term_detected:
        disable_channel_query = {
          'ManagementId':management_id, 
          'Disabled':True,
          'X-Emby-Token':API_KEY,
          'X-Emby-Language':'en-us',
          'reqformat':'json',
          }
        disable_channel = requests.post(SERVER_URL + '/emby/LiveTv/Manage/Channels/'+ id +'/Disabled',params=disable_channel_query)
        print(str(i) + " Disabled Channel: " + name + " (" + id + ")")
      else:
        print(str(i) + " Skipped Channel: " + name + " (" + id + ")")
  # END channel in channels['Items']:

  # Increment the channel_loop_index and get another batch of channels
  channel_loop_index += 30
  get_channels_response = requests.get(SERVER_URL + "/emby/LiveTv/Manage/Channels", params=get_channels_query)
  channels = get_channels_response.json()

# END while len(channels['Items']) > 0:

