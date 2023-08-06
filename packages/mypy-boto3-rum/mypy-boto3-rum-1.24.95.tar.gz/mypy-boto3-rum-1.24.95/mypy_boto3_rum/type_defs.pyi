"""
Type annotations for rum service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rum/type_defs/)

Usage::

    ```python
    from mypy_boto3_rum.type_defs import AppMonitorConfigurationTypeDef

    data: AppMonitorConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import MetricDestinationType, StateEnumType, TelemetryType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AppMonitorConfigurationTypeDef",
    "AppMonitorDetailsTypeDef",
    "AppMonitorSummaryTypeDef",
    "MetricDefinitionRequestTypeDef",
    "MetricDefinitionTypeDef",
    "ResponseMetadataTypeDef",
    "BatchDeleteRumMetricDefinitionsErrorTypeDef",
    "BatchDeleteRumMetricDefinitionsRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "BatchGetRumMetricDefinitionsRequestRequestTypeDef",
    "CwLogTypeDef",
    "DeleteAppMonitorRequestRequestTypeDef",
    "DeleteRumMetricsDestinationRequestRequestTypeDef",
    "QueryFilterTypeDef",
    "TimeRangeTypeDef",
    "GetAppMonitorRequestRequestTypeDef",
    "ListAppMonitorsRequestRequestTypeDef",
    "ListRumMetricsDestinationsRequestRequestTypeDef",
    "MetricDestinationSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RumEventTypeDef",
    "UserDetailsTypeDef",
    "PutRumMetricsDestinationRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "CreateAppMonitorRequestRequestTypeDef",
    "UpdateAppMonitorRequestRequestTypeDef",
    "BatchCreateRumMetricDefinitionsErrorTypeDef",
    "BatchCreateRumMetricDefinitionsRequestRequestTypeDef",
    "UpdateRumMetricDefinitionRequestRequestTypeDef",
    "BatchGetRumMetricDefinitionsResponseTypeDef",
    "CreateAppMonitorResponseTypeDef",
    "GetAppMonitorDataResponseTypeDef",
    "ListAppMonitorsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "BatchDeleteRumMetricDefinitionsResponseTypeDef",
    "BatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef",
    "ListAppMonitorsRequestListAppMonitorsPaginateTypeDef",
    "ListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef",
    "DataStorageTypeDef",
    "GetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef",
    "GetAppMonitorDataRequestRequestTypeDef",
    "ListRumMetricsDestinationsResponseTypeDef",
    "PutRumEventsRequestRequestTypeDef",
    "BatchCreateRumMetricDefinitionsResponseTypeDef",
    "AppMonitorTypeDef",
    "GetAppMonitorResponseTypeDef",
)

AppMonitorConfigurationTypeDef = TypedDict(
    "AppMonitorConfigurationTypeDef",
    {
        "AllowCookies": bool,
        "EnableXRay": bool,
        "ExcludedPages": Sequence[str],
        "FavoritePages": Sequence[str],
        "GuestRoleArn": str,
        "IdentityPoolId": str,
        "IncludedPages": Sequence[str],
        "SessionSampleRate": float,
        "Telemetries": Sequence[TelemetryType],
    },
    total=False,
)

AppMonitorDetailsTypeDef = TypedDict(
    "AppMonitorDetailsTypeDef",
    {
        "id": str,
        "name": str,
        "version": str,
    },
    total=False,
)

AppMonitorSummaryTypeDef = TypedDict(
    "AppMonitorSummaryTypeDef",
    {
        "Created": str,
        "Id": str,
        "LastModified": str,
        "Name": str,
        "State": StateEnumType,
    },
    total=False,
)

_RequiredMetricDefinitionRequestTypeDef = TypedDict(
    "_RequiredMetricDefinitionRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalMetricDefinitionRequestTypeDef = TypedDict(
    "_OptionalMetricDefinitionRequestTypeDef",
    {
        "DimensionKeys": Mapping[str, str],
        "EventPattern": str,
        "UnitLabel": str,
        "ValueKey": str,
    },
    total=False,
)

class MetricDefinitionRequestTypeDef(
    _RequiredMetricDefinitionRequestTypeDef, _OptionalMetricDefinitionRequestTypeDef
):
    pass

_RequiredMetricDefinitionTypeDef = TypedDict(
    "_RequiredMetricDefinitionTypeDef",
    {
        "MetricDefinitionId": str,
        "Name": str,
    },
)
_OptionalMetricDefinitionTypeDef = TypedDict(
    "_OptionalMetricDefinitionTypeDef",
    {
        "DimensionKeys": Dict[str, str],
        "EventPattern": str,
        "UnitLabel": str,
        "ValueKey": str,
    },
    total=False,
)

class MetricDefinitionTypeDef(_RequiredMetricDefinitionTypeDef, _OptionalMetricDefinitionTypeDef):
    pass

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

BatchDeleteRumMetricDefinitionsErrorTypeDef = TypedDict(
    "BatchDeleteRumMetricDefinitionsErrorTypeDef",
    {
        "ErrorCode": str,
        "ErrorMessage": str,
        "MetricDefinitionId": str,
    },
)

_RequiredBatchDeleteRumMetricDefinitionsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchDeleteRumMetricDefinitionsRequestRequestTypeDef",
    {
        "AppMonitorName": str,
        "Destination": MetricDestinationType,
        "MetricDefinitionIds": Sequence[str],
    },
)
_OptionalBatchDeleteRumMetricDefinitionsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchDeleteRumMetricDefinitionsRequestRequestTypeDef",
    {
        "DestinationArn": str,
    },
    total=False,
)

class BatchDeleteRumMetricDefinitionsRequestRequestTypeDef(
    _RequiredBatchDeleteRumMetricDefinitionsRequestRequestTypeDef,
    _OptionalBatchDeleteRumMetricDefinitionsRequestRequestTypeDef,
):
    pass

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredBatchGetRumMetricDefinitionsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetRumMetricDefinitionsRequestRequestTypeDef",
    {
        "AppMonitorName": str,
        "Destination": MetricDestinationType,
    },
)
_OptionalBatchGetRumMetricDefinitionsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetRumMetricDefinitionsRequestRequestTypeDef",
    {
        "DestinationArn": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class BatchGetRumMetricDefinitionsRequestRequestTypeDef(
    _RequiredBatchGetRumMetricDefinitionsRequestRequestTypeDef,
    _OptionalBatchGetRumMetricDefinitionsRequestRequestTypeDef,
):
    pass

CwLogTypeDef = TypedDict(
    "CwLogTypeDef",
    {
        "CwLogEnabled": bool,
        "CwLogGroup": str,
    },
    total=False,
)

DeleteAppMonitorRequestRequestTypeDef = TypedDict(
    "DeleteAppMonitorRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredDeleteRumMetricsDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteRumMetricsDestinationRequestRequestTypeDef",
    {
        "AppMonitorName": str,
        "Destination": MetricDestinationType,
    },
)
_OptionalDeleteRumMetricsDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteRumMetricsDestinationRequestRequestTypeDef",
    {
        "DestinationArn": str,
    },
    total=False,
)

class DeleteRumMetricsDestinationRequestRequestTypeDef(
    _RequiredDeleteRumMetricsDestinationRequestRequestTypeDef,
    _OptionalDeleteRumMetricsDestinationRequestRequestTypeDef,
):
    pass

QueryFilterTypeDef = TypedDict(
    "QueryFilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
    total=False,
)

_RequiredTimeRangeTypeDef = TypedDict(
    "_RequiredTimeRangeTypeDef",
    {
        "After": int,
    },
)
_OptionalTimeRangeTypeDef = TypedDict(
    "_OptionalTimeRangeTypeDef",
    {
        "Before": int,
    },
    total=False,
)

class TimeRangeTypeDef(_RequiredTimeRangeTypeDef, _OptionalTimeRangeTypeDef):
    pass

GetAppMonitorRequestRequestTypeDef = TypedDict(
    "GetAppMonitorRequestRequestTypeDef",
    {
        "Name": str,
    },
)

ListAppMonitorsRequestRequestTypeDef = TypedDict(
    "ListAppMonitorsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListRumMetricsDestinationsRequestRequestTypeDef = TypedDict(
    "_RequiredListRumMetricsDestinationsRequestRequestTypeDef",
    {
        "AppMonitorName": str,
    },
)
_OptionalListRumMetricsDestinationsRequestRequestTypeDef = TypedDict(
    "_OptionalListRumMetricsDestinationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListRumMetricsDestinationsRequestRequestTypeDef(
    _RequiredListRumMetricsDestinationsRequestRequestTypeDef,
    _OptionalListRumMetricsDestinationsRequestRequestTypeDef,
):
    pass

MetricDestinationSummaryTypeDef = TypedDict(
    "MetricDestinationSummaryTypeDef",
    {
        "Destination": MetricDestinationType,
        "DestinationArn": str,
        "IamRoleArn": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredRumEventTypeDef = TypedDict(
    "_RequiredRumEventTypeDef",
    {
        "details": str,
        "id": str,
        "timestamp": Union[datetime, str],
        "type": str,
    },
)
_OptionalRumEventTypeDef = TypedDict(
    "_OptionalRumEventTypeDef",
    {
        "metadata": str,
    },
    total=False,
)

class RumEventTypeDef(_RequiredRumEventTypeDef, _OptionalRumEventTypeDef):
    pass

UserDetailsTypeDef = TypedDict(
    "UserDetailsTypeDef",
    {
        "sessionId": str,
        "userId": str,
    },
    total=False,
)

_RequiredPutRumMetricsDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredPutRumMetricsDestinationRequestRequestTypeDef",
    {
        "AppMonitorName": str,
        "Destination": MetricDestinationType,
    },
)
_OptionalPutRumMetricsDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalPutRumMetricsDestinationRequestRequestTypeDef",
    {
        "DestinationArn": str,
        "IamRoleArn": str,
    },
    total=False,
)

class PutRumMetricsDestinationRequestRequestTypeDef(
    _RequiredPutRumMetricsDestinationRequestRequestTypeDef,
    _OptionalPutRumMetricsDestinationRequestRequestTypeDef,
):
    pass

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredCreateAppMonitorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppMonitorRequestRequestTypeDef",
    {
        "Domain": str,
        "Name": str,
    },
)
_OptionalCreateAppMonitorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppMonitorRequestRequestTypeDef",
    {
        "AppMonitorConfiguration": AppMonitorConfigurationTypeDef,
        "CwLogEnabled": bool,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateAppMonitorRequestRequestTypeDef(
    _RequiredCreateAppMonitorRequestRequestTypeDef, _OptionalCreateAppMonitorRequestRequestTypeDef
):
    pass

_RequiredUpdateAppMonitorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAppMonitorRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateAppMonitorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAppMonitorRequestRequestTypeDef",
    {
        "AppMonitorConfiguration": AppMonitorConfigurationTypeDef,
        "CwLogEnabled": bool,
        "Domain": str,
    },
    total=False,
)

class UpdateAppMonitorRequestRequestTypeDef(
    _RequiredUpdateAppMonitorRequestRequestTypeDef, _OptionalUpdateAppMonitorRequestRequestTypeDef
):
    pass

BatchCreateRumMetricDefinitionsErrorTypeDef = TypedDict(
    "BatchCreateRumMetricDefinitionsErrorTypeDef",
    {
        "ErrorCode": str,
        "ErrorMessage": str,
        "MetricDefinition": MetricDefinitionRequestTypeDef,
    },
)

_RequiredBatchCreateRumMetricDefinitionsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchCreateRumMetricDefinitionsRequestRequestTypeDef",
    {
        "AppMonitorName": str,
        "Destination": MetricDestinationType,
        "MetricDefinitions": Sequence[MetricDefinitionRequestTypeDef],
    },
)
_OptionalBatchCreateRumMetricDefinitionsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchCreateRumMetricDefinitionsRequestRequestTypeDef",
    {
        "DestinationArn": str,
    },
    total=False,
)

class BatchCreateRumMetricDefinitionsRequestRequestTypeDef(
    _RequiredBatchCreateRumMetricDefinitionsRequestRequestTypeDef,
    _OptionalBatchCreateRumMetricDefinitionsRequestRequestTypeDef,
):
    pass

_RequiredUpdateRumMetricDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRumMetricDefinitionRequestRequestTypeDef",
    {
        "AppMonitorName": str,
        "Destination": MetricDestinationType,
        "MetricDefinition": MetricDefinitionRequestTypeDef,
        "MetricDefinitionId": str,
    },
)
_OptionalUpdateRumMetricDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRumMetricDefinitionRequestRequestTypeDef",
    {
        "DestinationArn": str,
    },
    total=False,
)

class UpdateRumMetricDefinitionRequestRequestTypeDef(
    _RequiredUpdateRumMetricDefinitionRequestRequestTypeDef,
    _OptionalUpdateRumMetricDefinitionRequestRequestTypeDef,
):
    pass

BatchGetRumMetricDefinitionsResponseTypeDef = TypedDict(
    "BatchGetRumMetricDefinitionsResponseTypeDef",
    {
        "MetricDefinitions": List[MetricDefinitionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppMonitorResponseTypeDef = TypedDict(
    "CreateAppMonitorResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAppMonitorDataResponseTypeDef = TypedDict(
    "GetAppMonitorDataResponseTypeDef",
    {
        "Events": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppMonitorsResponseTypeDef = TypedDict(
    "ListAppMonitorsResponseTypeDef",
    {
        "AppMonitorSummaries": List[AppMonitorSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "ResourceArn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteRumMetricDefinitionsResponseTypeDef = TypedDict(
    "BatchDeleteRumMetricDefinitionsResponseTypeDef",
    {
        "Errors": List[BatchDeleteRumMetricDefinitionsErrorTypeDef],
        "MetricDefinitionIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredBatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef = TypedDict(
    "_RequiredBatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef",
    {
        "AppMonitorName": str,
        "Destination": MetricDestinationType,
    },
)
_OptionalBatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef = TypedDict(
    "_OptionalBatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef",
    {
        "DestinationArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class BatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef(
    _RequiredBatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef,
    _OptionalBatchGetRumMetricDefinitionsRequestBatchGetRumMetricDefinitionsPaginateTypeDef,
):
    pass

ListAppMonitorsRequestListAppMonitorsPaginateTypeDef = TypedDict(
    "ListAppMonitorsRequestListAppMonitorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef = TypedDict(
    "_RequiredListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef",
    {
        "AppMonitorName": str,
    },
)
_OptionalListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef = TypedDict(
    "_OptionalListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef(
    _RequiredListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef,
    _OptionalListRumMetricsDestinationsRequestListRumMetricsDestinationsPaginateTypeDef,
):
    pass

DataStorageTypeDef = TypedDict(
    "DataStorageTypeDef",
    {
        "CwLog": CwLogTypeDef,
    },
    total=False,
)

_RequiredGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef = TypedDict(
    "_RequiredGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef",
    {
        "Name": str,
        "TimeRange": TimeRangeTypeDef,
    },
)
_OptionalGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef = TypedDict(
    "_OptionalGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef",
    {
        "Filters": Sequence[QueryFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class GetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef(
    _RequiredGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef,
    _OptionalGetAppMonitorDataRequestGetAppMonitorDataPaginateTypeDef,
):
    pass

_RequiredGetAppMonitorDataRequestRequestTypeDef = TypedDict(
    "_RequiredGetAppMonitorDataRequestRequestTypeDef",
    {
        "Name": str,
        "TimeRange": TimeRangeTypeDef,
    },
)
_OptionalGetAppMonitorDataRequestRequestTypeDef = TypedDict(
    "_OptionalGetAppMonitorDataRequestRequestTypeDef",
    {
        "Filters": Sequence[QueryFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class GetAppMonitorDataRequestRequestTypeDef(
    _RequiredGetAppMonitorDataRequestRequestTypeDef, _OptionalGetAppMonitorDataRequestRequestTypeDef
):
    pass

ListRumMetricsDestinationsResponseTypeDef = TypedDict(
    "ListRumMetricsDestinationsResponseTypeDef",
    {
        "Destinations": List[MetricDestinationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRumEventsRequestRequestTypeDef = TypedDict(
    "PutRumEventsRequestRequestTypeDef",
    {
        "AppMonitorDetails": AppMonitorDetailsTypeDef,
        "BatchId": str,
        "Id": str,
        "RumEvents": Sequence[RumEventTypeDef],
        "UserDetails": UserDetailsTypeDef,
    },
)

BatchCreateRumMetricDefinitionsResponseTypeDef = TypedDict(
    "BatchCreateRumMetricDefinitionsResponseTypeDef",
    {
        "Errors": List[BatchCreateRumMetricDefinitionsErrorTypeDef],
        "MetricDefinitions": List[MetricDefinitionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AppMonitorTypeDef = TypedDict(
    "AppMonitorTypeDef",
    {
        "AppMonitorConfiguration": AppMonitorConfigurationTypeDef,
        "Created": str,
        "DataStorage": DataStorageTypeDef,
        "Domain": str,
        "Id": str,
        "LastModified": str,
        "Name": str,
        "State": StateEnumType,
        "Tags": Dict[str, str],
    },
    total=False,
)

GetAppMonitorResponseTypeDef = TypedDict(
    "GetAppMonitorResponseTypeDef",
    {
        "AppMonitor": AppMonitorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
