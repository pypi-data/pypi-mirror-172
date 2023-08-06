# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyter_capture_output']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0', 'ipykernel>=5.0.0', 'ipython>=6.0.0']

setup_kwargs = {
    'name': 'jupyter-capture-output',
    'version': '0.0.7',
    'description': 'Capture output from JupyterLab',
    'long_description': '# jupyter-caputure-output\nA cell magic that captures jupyter cell output\n\n\n[![JupyterLight](https://jupyterlite.rtfd.io/en/latest/_static/badge.svg)](https://octoframes.github.io/jupyter_capture_output/)  \n\n## Install\nRequires Python >=3.8\n```py\npip install jupyter_capture_output\n```\n\n\n## Example\n\nhttps://user-images.githubusercontent.com/44469195/184531492-6bc34ed9-3640-447b-b09e-767d01ecf3da.mov\n\n\n```py\nimport jupyter_capture_output\n```\n\n```py \n%%capture_text --path "foo.txt"\nprint("Hello World")\n```\n\n```py\nimport matplotlib.pyplot as plt\n```\n\n```py\n%%capture_img --path "foo.png bar.png"\nplt.plot([1,2],[10,20])\nplt.show()\nplt.plot([3,4],[-10,-20])\nplt.show()\n```\n\n```py\n%%capture_img  --path "foo.jpg bar.jpg" --compression 50\nplt.plot([1,2],[10,20], color = "r")\nplt.show()\nplt.plot([3,4],[-10,-20],color = "r")\nplt.show()\n```\n\n\n\nImplemented\n* `%%capture_text`  ->  to .txt file with text output\n* `%%capture_img` -> to .png or .jpg with image output\n* `%%capture_video` -> to .mp4 file with the video output\n\n## Wishlist\n\n* `%%capture_svg` ->  to .svg file with svg vectorgraphic outout\n* `%%capture_numpy_array` -> to .np file with array \n* `%%capture_csv` -> to .csv with datapoints \n* `%%capture_gif` -> to .gif with animation\n* `%%capture_auto`-> automatically detects what output there is to capture\n\n## Changelog\n\n### 0.0.8 (work in progress)\n\n### 0.0.7 \n\n* Add relative path support and automatically create paths if they don\'t exist yet.\n\nAdd some experimental magic, but this will likely be removed in future versions:\n* * `experimental_capture_video_first_last` captures video and extracts first and last frame from it. Useful for post-processing of videos in other video editors. Needs ffmpeg installed\n\n* `experimental_video_thumbnail` extracts video from the Jupyter cell output, and replaces it with an image thumbnail of the video -> useful for Version control. Needs matplotlib and ffmpeg installed\n### 0.0.6\n\nbetter regex in capture video\nchange example images to dogs\n\n### 0.0.5\n\nRemove debugging code\nAdd JupyterLiteDemo\n### 0.0.4\n\nAdd Text and Video capture cell magic\nupdate example\n\n### 0.0.3\n\nSetup automatic release action.\n\n### 0.0.2\n\nUpdate example\n\n### 0.0.1\n\nInitial release\n',
    'author': 'kolibril13',
    'author_email': '44469195+kolibril13@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
