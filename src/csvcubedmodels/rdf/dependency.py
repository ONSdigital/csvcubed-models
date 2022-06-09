"""
Dependency
----------

Defines a dependency between RDF graphs.
"""
from typing import Annotated, Optional

from rdflib import Literal

from csvcubedmodels.dataclassbase import DataClassBase
from csvcubedmodels.rdf.namespaces import VOID
from csvcubedmodels.rdf.triple import Triple
from csvcubedmodels.rdf.resource import NewResource, ExistingResource, PropertyStatus, map_resource_to_uri

class RdfGraphDependency(NewResource):
    """
    Define a dependency between the current RDF graph and another.
    """

    uri_space: Annotated[
        str, Triple(VOID.uriSpace, PropertyStatus.mandatory, Literal)
    ]
    """
    The URI prefix which specifies which URIs can be dereferenced with this dependency. 
    
    See <https://www.w3.org/TR/void/#pattern> for more detail.
    """

    dependent_rdf_file_location: Annotated[
        Optional[ExistingResource],
        Triple(VOID.dataDump, PropertyStatus.recommended, map_resource_to_uri),
    ]
    """
    The URI location of the dependent RDF file containing triples.
    """

    sparql_end_point: Annotated[
        Optional[ExistingResource],
        Triple(VOID.sparqlEndpoint, PropertyStatus.optional, map_resource_to_uri),
    ]
    """
    The URI location of a SPARQL end point where identifiers can be dereferenced. 
    """

    def __init__(self, uri: str):
        NewResource.__init__(self, uri)
        self.rdf_types.add(VOID.Dataset)
