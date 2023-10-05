import http.client
import requests
import json


def upload_image(dialog_id, oauth_code, image_url=None, image=None):
    if not image_url is None:
        headers = {
            'Authorization': f'OAuth {oauth_code}',
            'Content-Type': 'application/json'
        }
        data = {
            'url': image_url
        }
        img_data = json.dumps(data)

        response = requests.post(f'https://dialogs.yandex.net/api/v1/skills/{dialog_id}/images', data=img_data,
                                 headers=headers)

    elif not image is None:
        headers = {
            'Authorization': f'OAuth {oauth_code}',
        }

        response = requests.post(f'https://dialogs.yandex.net/api/v1/skills/{dialog_id}/images', files={'file': image},
                                 headers=headers)

    if response.status_code in [201, 200]:
        json_response = json.loads(response.content.decode('utf-8'))
        return json_response

        """
        Пример json_response
        {
          "image": {
            "id": <идентификатор изображения>,
            "origUrl": <URL изображения>,
            "size": <размер изображения>,
            "createdAt": <дата загрузки>
          }
        }
        """

    else:
        return f"Ошибка HTTP: {response.status_code}, {response.reason}"


def get_uploaded_images(dialog_id, oauth_code):
    connection = http.client.HTTPSConnection('dialogs.yandex.net')

    headers = {
        'Authorization': f'OAuth {oauth_code}',
    }

    connection.request('GET', f'/api/v1/skills/{dialog_id}/images', headers=headers)
    response = connection.getresponse()

    if response.status in [201, 200]:
        json_response = json.loads(response.read().decode('utf-8'))
        return json_response

        """
        {
          "images": [
            {
              "id": <идентификатор изображения>,
              "origUrl": <URL изображения>,
              "size": <размер изображения>,
              "createdAt": <дата загрузки>
            },
            ...
          ],
          "total": <количество загруженных изображений>
        } 
        """

    else:
        return f"Ошибка HTTP:, {response.status}, {response.reason}"


def delete_image(dialog_id, oauth_code, image_id=None, image_url=None):
    connection = http.client.HTTPSConnection('dialogs.yandex.net')

    headers = {
        'Authorization': f'OAuth {oauth_code}',
    }

    if not image_id is None:
        connection.request('DELETE', f'/api/v1/skills/{dialog_id}/images/{image_id}', headers=headers)
        response = connection.getresponse()
        return f"{response.status}, {response.reason}"

    elif not image_url is None:
        images_list = get_uploaded_images(dialog_id, oauth_code).get('images')

        for image in images_list:
            if image['origUrl'] == image_url:
                image_id = image['id']

                connection.request('DELETE', f'/api/v1/skills/{dialog_id}/images/{image_id}', headers=headers)
                response = connection.getresponse()
                return f"{response.status}, {response.reason}"


    else:
        return f"Ошибка `delete_image`: нет `image_id` и `image_url`"