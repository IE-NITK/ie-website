# IE-Website
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Install components
```bash
sudo apt-get update
sudo apt-get install python-pip 
```

### Setting up Virtual Environment and Install Requirements
```bash
sudo pip install virtualenv
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements-local.txt
```

### Running the website locally
```bash
Update settings.py:
  1. Make DEBUG = True
  2. In DATABASES option , uncomment the commented and comment the uncomment 
cd ~/ie-website
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/chaitany10"><img src="https://avatars1.githubusercontent.com/u/32352441?v=4" width="100px;" alt=""/><br /><sub><b>Chaitany Pandiya</b></sub></a><br /><a href="https://github.com/IE-NITK/ie-website/commits?author=chaitany10" title="Code">💻</a></td>
    <td align="center"><a href="http://madhumithanara.github.io"><img src="https://avatars2.githubusercontent.com/u/38850744?v=4" width="100px;" alt=""/><br /><sub><b>madhumithanara</b></sub></a><br /><a href="https://github.com/IE-NITK/ie-website/commits?author=madhumithanara" title="Code">💻</a></td>
    <td align="center"><a href="http://krahulreddy.github.io"><img src="https://avatars2.githubusercontent.com/u/31247036?v=4" width="100px;" alt=""/><br /><sub><b>K Rahul Reddy</b></sub></a><br /><a href="https://github.com/IE-NITK/ie-website/commits?author=krahulreddy" title="Code">💻</a> <a href="#design-krahulreddy" title="Design">🎨</a></td>
    <td align="center"><a href="https://github.com/Paranjaysaxena"><img src="https://avatars0.githubusercontent.com/u/42527319?v=4" width="100px;" alt=""/><br /><sub><b>Paranjaysaxena</b></sub></a><br /><a href="https://github.com/IE-NITK/ie-website/commits?author=Paranjaysaxena" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!