# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['symmetric_synthetic']

package_data = \
{'': ['*']}

install_requires = \
['click',
 'numpy>=1.21.0,<2.0.0',
 'pillow>=9.1.0,<10.0.0',
 'scikit-image>=0.17.2,<0.18.0',
 'scipy>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['symmsyn = symmetric_synthetic.data_process:main']}

setup_kwargs = {
    'name': 'symmetric-synthetic',
    'version': '0.1.0',
    'description': 'create symmetrical objects in synthetic images and their corresponding mask',
    'long_description': '<!--\nSPDX-FileCopyrightText: 2022 Venkatesh Danush Kumar <Danush-Kumar.Venkatesh@student.tu-freiberg.de>, Peter Steinbach <p.steinbach@hzdr.de>\n\nSPDX-License-Identifier: BSD-3-Clause-Attribution\n-->\n\n# Shape generate\n\nThe file ```shape_generate.py``` has multiple functionality to create synthetic dataset\nof symmetrical objects. The methods creates two folders, namely, ```images``` and ```masks```. The images are constructed from the Gaussain distribution.\n\n# Installation\n\nThis repo is managed with `poetry`. To try out this package, do:\n\n```\n$ poetry install\n$ poetry run symmsyn --help\n```\n\n# Examples\n\nThe following examples show the method to create the dataset\n\n1. Create a dataset of `200` images of size=256 x 256 with circle objects of radius=`10` and density=`20`\n```bash\npoetry run symmsyn --job_type "single" --n_image 200 --folder_name "circle_data" --object_type "circle" --image_dims 256 --circle_radius 10 --start_count 45 --end_count 50\n```\n\n2. Create a dataset of `100` images of size=512 x 512 with square objects of side=`10`, density=`35`\n```bash\npoetry run symmsyn --job_type "single" --n_image 100 --folder_name "square_data" --object_type "square" --image_dims 512 --start_count 34 --end_count 35 --square_size 10 10\n```\n\n3. Create a dataset of `100` images of size=512 x 512 with triangle objects of varying size, density=`35`\n```bash\npoetry run symmsyn --job_type "single" --n_image 100 --folder_name "triangle_data" --object_type "triangle" --image_dims 512 --start_count 34 --end_count 35 --size_vary True\n```\n\n4. Create a dataset of `500` images of size=256 x 256 with circle+ellipse objects of radius=`10`, minor_radius=`5`, major_radius=`10`, circle density=`35`, ellipse density=`10`\n\nThe elliptical objects will be equally divided into horizontal and angular objects. Specify ```angle``` parameter if needed. \n```bash\npoetry run symmsyn --job_type "multi" --n_image 100 --folder_name "circle_ellipse_data" --image_dims 256 --circle_radius 10 --circle_start 34 --circle_end 35 --add_ellipse True --ell_count 10 --m_radius 10 --n_radius 5 --ell_angle 45\n```\n\n5. Create a dataset of `500` images of size=256 x 256 with circle+ellipse+triangle objects of varying sizes and circle density=`10`, ellipse density=`10`, triangle density=`40`\n\nThe elliptical objects will be equally divided into horizontal and angular objects. Specify ```angle``` parameter if needed. \n```bash\npoetry run symmsyn --job_type "multi" --n_image 500 --folder_name "circle_ellipse_tri_data" --image_dims 256 --circle_start 9 --circle_end 10 --add_tri True --add_ellipse True --tri_count 40 --ell_count 10 --size_vary True\n```\n\n6. Create a dataset of `500` images of size=256 x 256 with circle+square+triangle objects of radius=`10`, side=`10`, size=`12` and circle density=`10`, square density=`10`, triangle density=`15` and change the intensity of objects to `0.5*std.` of the background\n\nTo change from square to rectangle objects vary the values in the parameter ```size```, a good starting value (-8,12) \n```bash\npoetry run symmsyn --job_type "multi" --n_image 500 --folder_name "circle_square_tri_data" --image_dims 256 --circle_radius 10 --circle_start 9 --circle_end 10 --add_square True --add_tri True --square_size 10 10 --tri_size 12 12 --sq_count 10 --tri_count 15 --intensity_vary True --intensity_ratio 0.5\n```\n\n7. Create only an image and mask size=256 x 256 with circle+square+triangle objects of radius=10,side=10, size=12 and circle density=10, square density=10, triangle density=15 \n\nThe image and mask are saved as a file "multi.png"\n\nTo change from square to rectangle objects vary the values in the parameter ```size```, a good starting value (-8,12) \n```bash\npoetry run symmsyn --job_type "multi" --image_dims 256 --circle_radius 10 --circle_start 9 --circle_end 10 --add_square True --add_tri True --square_size 10 10 --tri_size 12 12 --sq_count 10 --tri_count 15 --save_file False\n```\n=================================================================================================================================================================\n\nSome **example images** are shown here.\n\n\n![alt text](https://github.com/danushv07/symmetric_synthetic/blob/main/images/initial_dataset.png)\n\nThe datasets in the order from left to right: circle objects, circle and ellipse, circle and square, circle, ellipse and triangle objects.\n\nAn example of circle, ellipse and triangle object dataset with the variation of signal to noise.\n\n![alt text](https://github.com/danushv07/symmetric_synthetic/blob/main/images/noisy_dataset.png)\n',
    'author': 'Danush Kumar Venkatesh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danushv07/symmetric_synthetic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
