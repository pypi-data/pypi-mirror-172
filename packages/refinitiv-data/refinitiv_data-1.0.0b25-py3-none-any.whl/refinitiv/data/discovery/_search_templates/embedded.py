import pandas as pd

from refinitiv.data.content.search import Views
from refinitiv.data.discovery._search_templates.base import SearchTemplate


class RICCategoryTemplate(SearchTemplate):
    """Returns the category for a given RIC"""

    def __init__(self):
        super().__init__(
            name="RICCategory",
            pass_through_defaults={
                "view": Views.QUOTES_AND_STIRS,
                "select": 'RCSAssetCategoryLeaf',
                "top": 1,
            },
            filter="RIC eq '#{ric}'",
        )

    def _search_kwargs(self, *, ric, **kwargs) -> dict:
        return super()._search_kwargs(ric=ric, **kwargs)

    def search(self, *, ric, **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame
        
        Parameters
        ----------
        ric
            The RIC for which to search the category.

        Returns
        -------
        DataFrame
        """
        return super().search(ric=ric, **kwargs)


class UnderlyingRICToOptionTemplate(SearchTemplate):
    """Simple search for options on any underlying"""

    def __init__(self):
        super().__init__(
            name="UnderlyingRICToOption",
            pass_through_defaults={
                "view": Views.SEARCH_ALL,
                "select": 'RIC,DTSubjectName,ExpiryDateString,StrikePrice,CallPutOption,ContractType,Currency',
                "order_by": 'ExpiryDate,StrikePrice,CallPutOption',
                "top": 100,
            },
            filter="UnderlyingQuoteRIC eq '#{ric}' and RCSAssetCategoryLeaf eq 'Option' and IsChain eq false",
        )

    def _search_kwargs(self, *, ric, **kwargs) -> dict:
        return super()._search_kwargs(ric=ric, **kwargs)

    def search(self, *, ric, **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame
        
        Parameters
        ----------
        ric
            The underlying instrument for which to search for options.

        Returns
        -------
        DataFrame
        """
        return super().search(ric=ric, **kwargs)


class UnderlyingRICToFutureTemplate(SearchTemplate):
    """Simple search for futures on any underlying"""

    def __init__(self):
        super().__init__(
            name="UnderlyingRICToFuture",
            pass_through_defaults={
                "view": Views.SEARCH_ALL,
                "select": 'RIC,DTSubjectName,ExpiryDateString,ContractType,Currency',
                "order_by": 'ExpiryDate',
                "top": 100,
            },
            filter="UnderlyingQuoteRIC eq '#{ric}' and RCSAssetCategoryLeaf eq 'Future' and IsChain eq false and AssetStateName eq 'Active'",
        )

    def _search_kwargs(self, *, ric, **kwargs) -> dict:
        return super()._search_kwargs(ric=ric, **kwargs)

    def search(self, *, ric, **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame
        
        Parameters
        ----------
        ric
            The underlying instrument for which to search for futures.

        Returns
        -------
        DataFrame
        """
        return super().search(ric=ric, **kwargs)


class RICToIssuerTemplate(SearchTemplate):
    """Find issuer of a RIC"""

    def __init__(self):
        super().__init__(
            name="RICToIssuer",
            pass_through_defaults={
                "view": Views.SEARCH_ALL,
                "select": 'DTSubjectName,RCSIssuerCountryLeaf,IssuerOAPermID,PrimaryRIC',
            },
            filter="RIC eq '#{ric}'",
        )

    def _search_kwargs(self, *, ric, **kwargs) -> dict:
        return super()._search_kwargs(ric=ric, **kwargs)

    def search(self, *, ric, **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame
        
        Parameters
        ----------
        ric
            The RIC for which to search the issuer.

        Returns
        -------
        DataFrame
        """
        return super().search(ric=ric, **kwargs)


class OrganisationPermIDToUPTemplate(SearchTemplate):
    """Find ultimate parent of an organisation"""

    def __init__(self):
        super().__init__(
            name="OrganisationPermIDToUP",
            pass_through_defaults={
                "view": Views.SEARCH_ALL,
                "select": 'UltimateParentCompanyOAPermID,UltimateParentOrganisationName',
            },
            filter="OAPermID eq '#{entity_id}'",
        )

    def _search_kwargs(self, *, entity_id, **kwargs) -> dict:
        return super()._search_kwargs(entity_id=entity_id, **kwargs)

    def search(self, *, entity_id, **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame
        
        Parameters
        ----------
        entity_id
            PermID of the organisation.

        Returns
        -------
        DataFrame
        """
        return super().search(entity_id=entity_id, **kwargs)


class MinesTemplate(SearchTemplate):
    """Find coordinates of mines in a region"""

    def __init__(self):
        super().__init__(
            name="Mines",
            pass_through_defaults={
                "select": 'RIC,DTSubjectName,Latitude,Longitude,PhysicalAssetStatus',
                "top": 100,
                "skip": 0,
                "group_count": 3,
                "view": Views.PHYSICAL_ASSETS,
            },
            filter="RCSAssetTypeLeaf eq 'Mine' and RCSCommodityTypeLeaf xeq '#{commodity}' and RCSRegionLeaf eq '#{region}'",
        )

    def _search_kwargs(self, *, commodity='Gold', region='South Africa',
                       **kwargs) -> dict:
        return super()._search_kwargs(commodity=commodity, region=region, **kwargs)

    def search(self, *, commodity='Gold', region='South Africa',
               **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame
        
        Parameters
        ----------
        commodity
            Commodity extracted from the mine

        region
            Region to search in

        Returns
        -------
        DataFrame
        """
        return super().search(commodity=commodity, region=region, **kwargs)


class VesselsBoundForTemplate(SearchTemplate):
    """Search for vessels heading to a destination"""

    def __init__(self):
        super().__init__(
            name="VesselsBoundFor",
            pass_through_defaults={
                "order_by": 'GrossTonnage desc',
                "select": 'RIC,DTSubjectName,DTSimpleType,Latitude,Longitude,AISStatus,GrossTonnage',
                "top": 200,
                "skip": 0,
                "group_count": 3,
                "view": Views.VESSEL_PHYSICAL_ASSETS,
            },
            filter="DestinationPort eq '#{destination}' and AISStatus ne null and AISStatus ne 'Moored' and AISStatus ne '*defined*'",
        )

    def _search_kwargs(self, *, destination='Le Havre', **kwargs) -> dict:
        return super()._search_kwargs(destination=destination, **kwargs)

    def search(self, *, destination='Le Havre', **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame
        
        Parameters
        ----------
        destination
            Vessel's destination

        Returns
        -------
        DataFrame
        """
        return super().search(destination=destination, **kwargs)
