<div align="center">

<h1>uvp-web</h1>
<h3>Urban Video Project's web app for immersive media presentations</h3>
<!-- <h3>Urban Video Project's cross-platform immersive media player</h3> -->
<i><a href="https://www.lightwork.org/uvp">Urban Video Project</a> is a program of <a href="https://www.lightwork.org">Light Work</a> in partnership with the <a href="https://everson.org">Everson Museum of Art.</a></i>

<h1></h1>

<p align="center">

<a href="https://github.com/garytyler/uvp-web/actions">
  <img alt="Actions Status" src="https://github.com/garytyler/uvp-web/actions/workflows/test.yml/badge.svg">
</a>

<a href="https://codecov.io/gh/garytyler/uvp-web">
  <img src="https://codecov.io/gh/garytyler/uvp-web/branch/master/graph/badge.svg?token=XKGC0JOIIT"/>
</a>

<img alt="MIT" src="https://img.shields.io/github/license/garytyler/uvp-web">

</div>

# Overview

This web application facilitates live/in-person audience interaction with immersive media/360 video presentations via audience members' mobile devices. For use with [UVP Media Player](https://github.com/garytyler/uvp-media-player).

# Development

## .env template

```sh
DOMAIN_DEV=
DOMAIN_PROD=
DOMAIN_STAG=
LETSENCRYPT_EMAIL=

# API profile
PROJECT_NAME=
PROJECT_DESCRIPTION=

# API options
DEBUG=false
INSTALL_DEV=false

# Security
SECRET_KEY=
ALLOWED_HOSTS=
BACKEND_CORS_ORIGINS=

# Postgres
POSTGRES_USER=
POSTGRES_PASSWORD=

# PgAdmin
PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=
```
