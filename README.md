# kodak

HTTP server for handling image uploads and thumbnail generation.

This project requires [Poetry 1.0+](https://python-poetry.org/)

## Implementation goals

Support token based authentication:

```
POST /auth/token

GET /img/abcdefg.jpg?token=XYZ
```

Support dynamic resolution generation:

```
GET /img/abcdefg/100x50.jpg
```

Support server-side aliasing of resolutions to names:

```
GET /img/abcdefg/foobar.jpg  # translates to something like 120x90
```

Support parameter-based selection of scaling method:

```
# "absolute scale horizontal", "relative scale vertical"
GET /img/abcdefg/200x100.jpg?h=abs&v=rel
```

Support both sqlite and maria storage backend

Support redis caching to relieve file system strain

Support autocleaning of cached file system files to reduce directory size

Support
