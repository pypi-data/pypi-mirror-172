# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['msspeech']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0', 'aiohttp>=3.8.1,<4.0.0', 'click>=8.0.2,<9.0.0']

entry_points = \
{'console_scripts': ['msspeech = msspeech.__main__:main',
                     'msspeech-update-voices = msspeech.__main__:update_voices',
                     'msspeech_update_voices = '
                     'msspeech.__main__:update_voices']}

setup_kwargs = {
    'name': 'msspeech',
    'version': '3.7.9',
    'description': 'not official API for Microsoft speech synthesis from Microsoft Edge web browser read aloud',
    'long_description': '# msspeech\nnot official API for Microsoft speech synthesis from Microsoft Edge web browser read aloud\n\n## Installation\n\n`pip install --upgrade msspeech`\n\nor\n\n`poetry add msspeech`\n\n\nAfter updating an already installed library\nTo update the list of voices, run the command in your terminal:\n\n`msspeech-update-voices`\n\nor\n\n`poetry run msspeech-update-voices`\n\n\n## Notes\n### Bad news\n\nSince the first of July 2022,\nthe list of voices and the API as a whole has been very much limited!\n\n### But there is also good news\n\nThey returned back some male voices and added new languages, as well as made support for emotional styles.\nDespite the fact that styles appeared in JSON, you still won\'t be able to use them, SSML does not perceive them.\nSSML is very limited here, so there is no point in supporting it.\n\nThe official documentation is not suitable for this API. It seems this API uses **undocumented** SSML markup.\n\nhttps://docs.microsoft.com/ru-ru/azure/cognitive-services/speech-service/language-support#text-to-speech\n\n## Using\nthe pitch and rate values are set as a percentage from -100 to +100,\nthat is, it can be a negative, positive number, or zero for the default value.\n\nexamples: -30, 40, 0\n\n\nThe volume should be a fractional number from 0.1 to 1.0, but in fact it doesn\'t work for some reason.\n\n\nThe maximum synthesize text length is approximately 31000 characters per request.\n\n### from CLI\n\nsynthesize text:\n\n`msspeech Guy hello --filename audio.mp3`\n\nupdate voices list:\n\n`msspeech-update-voices`\n\n### From python\n```python\nimport asyncio\nfrom msspeech import MSSpeech\n\n\nasync def main():\n\tmss = MSSpeech()\n\tprint("Geting voices...")\n\tvoices = await mss.get_voices_list()\n\tprint("searching Russian voice...")\n\tfor voice in voices:\n\t\tif voice["Locale"] == "ru-RU":\n\t\t\tprint("Russian voice found:", voice["FriendlyName"])\n\t\t\tawait mss.set_voice(voice["Name"])\n\n\n\tprint("*" * 10)\n\tfilename = "audio.mp3"\n\t# with open("s.txt", encoding="UTF8") as f: text:str = f.read()\n\ttext = "Или написать текст здесь"\n\tprint("waiting...")\n\tawait mss.set_rate(1)\n\tawait mss.set_pitch(0)\n\tawait mss.set_volume(1)\n\tawait mss.synthesize(text.strip(), filename)\n\tprint("*"*10)\n\tprint("SUCCESS! OK!")\n\tprint("*"*10)\n\nif __name__ == "__main__":\n\tasyncio.run(main())\n```\n',
    'author': 'Alexey',
    'author_email': 'aleks-samos@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alekssamos/msspeech',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
