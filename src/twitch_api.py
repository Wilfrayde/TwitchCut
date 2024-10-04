import requests
import logging
from datetime import datetime, timedelta

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitchAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://api.twitch.tv/helix'
        self.token = self.get_access_token()
        self.headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.token}'
        }

    def get_access_token(self):
        logger.info('Obtention du jeton d\'accès...')
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            logger.info('Jeton d\'accès obtenu avec succès.')
            return access_token
        else:
            logger.error('Erreur lors de l\'obtention du jeton d\'accès.')
            raise Exception('Impossible d\'obtenir le jeton d\'accès.')

    def get_live_streamers(self, language='fr', first=10):
        logger.info('Récupération des streamers en direct...')
        url = f'{self.base_url}/streams'
        params = {
            'first': first,
            'language': language
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            streams_data = response.json()['data']
            logger.info(f'{len(streams_data)} streamers en direct récupérés.')
            return [stream['user_id'] for stream in streams_data]
        else:
            error_message = response.json().get('message', 'Erreur inconnue')
            logger.error(f'Erreur lors de la récupération des streamers : {error_message}')
            raise Exception(f'Impossible de récupérer les streamers : {error_message}')

    def get_top_clips(self, broadcaster_ids, period='day', first=10):
        logger.info(f'Récupération des meilleurs clips pour la période : {period}')
        url = f'{self.base_url}/clips'

        now = datetime.utcnow()
        if period == 'day':
            started_at = now - timedelta(days=1)
        elif period == 'week':
            started_at = now - timedelta(weeks=1)
        elif period == 'month':
            started_at = now - timedelta(days=30)
        else:
            started_at = None

        clips = []
        for broadcaster_id in broadcaster_ids:
            params = {
                'broadcaster_id': broadcaster_id,
                'first': first
            }

            if started_at:
                params['started_at'] = started_at.strftime('%Y-%m-%dT%H:%M:%SZ')
                params['ended_at'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')

            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                clips_data = response.json()['data']
                logger.info(f'{len(clips_data)} clips récupérés pour le streamer {broadcaster_id}.')
                for clip in clips_data:
                    clips.append({
                        'id': clip['id'],
                        'title': clip['title'],
                        'url': clip['url'],
                        'embed_url': clip['embed_url'],
                        'thumbnail_url': clip['thumbnail_url'],
                        'broadcaster_name': clip['broadcaster_name'],
                        'created_at': clip['created_at'],
                        'view_count': clip['view_count'],
                    })
            else:
                error_message = response.json().get('message', 'Erreur inconnue')
                logger.error(f'Erreur lors de la récupération des clips pour {broadcaster_id} : {error_message}')

        return clips