from database.db import fetch_cmoa_results, delete_title


def get_cmoa_results() -> list[dict]:
    titles = fetch_cmoa_results()

    if not titles:
        raise ValueError('Titles not found.')
    
    return [
        {'id': title[0].id,
        'url': title[0].url,
        'img_url': title[0].img_url,
        'release_date': title[0].release_date}
        for title in titles
    ]


def serve_delete_title(id: str):
    deleted = delete_title(id)
    if deleted:
        return {'deleted': True, 'msg': f'Title-{id} has been deleted.'}
    return {'deleted': False, 'msg': f'Title-{id} has not been found.'}