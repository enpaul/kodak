# kodak

Web server for auto-generating banners, previews, thumbnails, and more from any directory.
Lightweight, simple, and designed for performance.

Developed with [Poetry 1.0+](https://python-poetry.org/)

## Goals

- Support defining server-side manipulation specifications

  ```
  KODAK_MANIP_FOOBAR_CROP_VERTICAL=300
  KODAK_MANIP_FOOBAR_SCALE_HORIZONTAL=1200
  KODAK_MANIP_FOOBAR_SCALE_STRATEGY=absolute

  KODAK_MANIP_FIZZBUZZ_NAME=black+white
  KODAK_MANIP_FIZZBUZZ_BLACK_AND_WHITE=true
  KODAK_MANIP_FIZZBUZZ_SCALE_HORIZONTAL=50
  KODAK_MANIP_FIZZBUZZ_SCALE_STRATEGY=relative
  ```

- Support retrieving manipulated images based on server side configuration

  ```
  GET /image/<name>/foobar

  GET /image/<name>/black+white
  ```

- Support optionally exposing full-resolution source images

  ```
  GET /image/<name>/original
  ```

- Support caching of generated image manipulations for reuse

- Support [HTTP 410](https://httpstatuses.com/410) for indicating removed images and
  manipulations

- Support optional authentication with pre-generated access tokens

- Support static file tree management for exposure via external web server (which is faster
  than serving files with python)

- Support automatic indexing of newly added image files

- Support automatic indexing of removed image files

- Support arbitrary source directory structure

- Support Dockerized deployment

- Support bare-metal deployment (via systemd)

## Non-goals

- Client-defined image manipulations through publicly exposed parameters

  > Manipulating images is- in the grand scheme of things- pretty resource intensive. Exposing
  > dynamic parameters that can be cycled through to generate hundreds or thousands of
  > permutations for every known image on a server could be used to either consume the
  > server's entire disk or server's entire CPU.

- Upload functionality

  > This application should be as simple as possible. Lots of people have implemented file
  > upload systems, synchronizers, and managers way better than I have.

- Robust and flexible access control

  > See above. Complex authentication can be added using a reverse proxy or any one of several
  > dozen options for 3rd party middleware. The provided authentication is supposed to be
  > dead simple for people who absolutely need the server to be private but absolutely cannot
  > implement something more complicated.

- Pre-creation of image manipulations

  > The goal of this program is just-in-time creation of the manipulated assets with
  > aggressive caching; first load is slow, subsequent loads are fast. For this use case
  > there's no sense creating or storing an asset until it's known to be needed.
