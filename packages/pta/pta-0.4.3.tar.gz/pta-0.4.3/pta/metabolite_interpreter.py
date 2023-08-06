"""Parsing and identification of metabolites."""

from enum import Enum, auto

from .metabolite import Metabolite


class CompartmentConvention(Enum):
    """The convention used to define the compartment of a metabolite."""

    UNDERSCORE = auto()
    """The metabolite ID ends with "_<compartment_ID>" (e.g. g6p_c).
    """

    ASSUME_CYTOSOL = auto()
    """The compartment is not specified, all metabolites are assumed to belong to the
    cytosol.
    """


class Namespace(Enum):
    """The namespace in which metabolite identifiers are defined."""

    UNSPECIFIED = auto()
    """The namespace is not specified. In most cases PTA can find the metabolite
    in eQuilibrator even if the namespace is not specified. However, this is not
    guaranteed and it is recommended to always specify a namespace.
    """
    BIGG = auto()
    """Assume that metabolite identifiers belong to the BiGG namespace.
    """
    NONE = auto()
    """The identifiers do not represent actual metabolites.
    """


class MetaboliteInterpreter:
    """
    An interpreter used to transform metabolite IDs to compound identifiers that can be
    understood by eQuilibrator and compartment identifiers. Note: this class
    could/should partially replaced by cobrapy's functionalities if/when this feature is
    implemented: https://github.com/opencobra/cobrapy/issues/967

    Parameters
    ----------
    compartment_convention : CompartmentConvention, optional
        Naming convention used to specify metabolite and compartment identifiers, by
        default CompartmentConvention.UNDERSCORE.
    namespace : Namespace, optional
        Namespace in which the metabolite identifiers are defined, by default
        Namespace.BIGG.
    """

    def __init__(
        self,
        compartment_convention: CompartmentConvention = CompartmentConvention.UNDERSCORE,
        namespace: Namespace = Namespace.BIGG,
    ):
        self.compartment_convention = compartment_convention
        self.namespace = namespace

    def read(self, metabolite_id: str) -> Metabolite:
        """Parses a metabolite from a string, reading its identifier and
        compartment.

        Parameters
        ----------
        metabolite_name : str
            The identifier of a metabolite.

        Returns
        -------
        Metabolite
            Object describing the parsed metabolite. Note that only the identifier and
            compartment are set, the remaining fields (such as the charge) have to be
            specified manually.

        Raises
        ------
        Exception
            If the naming convention or namespace of the metabolite are not supported.
        """

        metabolite_key = ""
        compartment = ""

        if self.compartment_convention == CompartmentConvention.UNDERSCORE:
            assert "_" in metabolite_id, (
                "Metabolite identifier does not appear to follow the UNDERSCORE "
                "convention. You may need to specify a different convention."
            )
            (metabolite_key, compartment) = metabolite_id.rsplit("_", 1)
        elif self.compartment_convention == CompartmentConvention.ASSUME_CYTOSOL:
            metabolite_key = metabolite_id
            compartment = "c"
        else:
            raise Exception(
                f"Unsupported compartment convention: {self.compartment_convention}"
            )

        if self.namespace == Namespace.UNSPECIFIED:
            pass
        elif self.namespace == Namespace.BIGG:
            metabolite_key = "bigg.metabolite:" + metabolite_key
        elif self.namespace == Namespace.NONE:
            metabolite_key = "pseudometabolite:" + metabolite_key
        else:
            raise Exception(f"Unsupported namespace: {self.namespace}")

        return Metabolite(metabolite_id, metabolite_key, compartment)

    @property
    def compartment_convention(self) -> CompartmentConvention:
        """Gets the convention used to specify compartments."""
        return self._compartment_convention

    @compartment_convention.setter
    def compartment_convention(self, value: CompartmentConvention):
        """Sets the convention used to specify compartments."""
        self._compartment_convention = value

    @property
    def namespace(self) -> Namespace:
        """Gets the namespace of the metabolite names."""
        return self._namespace

    @namespace.setter
    def namespace(self, value: Namespace):
        """Sets the namespace of the metabolite names."""
        self._namespace = value
