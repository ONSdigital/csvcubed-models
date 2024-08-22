# csvcubed - models

> Models shared by multiple packages in the csvcubed family.

Part of the [csvcubed](https://github.com/GSS-Cogs/csvcubed/) project.

This package contains functionality to:

* Support serialisation of python models to RDF
* Provide models for relevant RDF ontologies such as [SKOS](http://www.w3.org/TR/skos-primer), [qb](https://www.w3.org/TR/vocab-data-cube/) and [DCAT](https://www.w3.org/TR/vocab-dcat-2/).
* Enable deserialisation of JSON to instances of python dataclasses.

## Adding a package

Dependencies are installed in the [Docker container](./Dockerfile) on a container-wide basis. If you're adding a new package, first run:

```bash
poetry add <some-package>
```

And once that has completed, if you are working inside the docker dev container, you must rebuild the container before the packages will be available for your use.

Copyright 2024 Office for National Statistics, under Crown Copyright 
