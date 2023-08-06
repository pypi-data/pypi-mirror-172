from logging import getLogger
from typing import Dict, List, Union, cast

import boto3

logger = getLogger(__name__)


def resource_generator(client, function_name: str, resource_name: str, **kwargs):
    paginator = client.get_paginator(function_name)
    for page in paginator.paginate(**kwargs):
        for resource in page[resource_name]:
            yield resource


def resource_lookup_by_tag(
    tags: Dict[str, Union[str, List[str]]], resource_types: List[str], region: str, session=False
):

    logger.debug(
        f"Retrieving resources (filtered by resource_types ({resource_types})) by tags {tags} and region {region}"
    )

    # Allow session override for assume role/cross account calls.
    if not session:
        session = boto3.session.Session()

    lookup_client = session.client("resourcegroupstaggingapi", region_name=region)

    # Convert tag object into expected tag list.
    tag_set = []
    for key, value in tags.items():
        if isinstance(value, list):
            tag_values = value
        else:
            tag_values = [value]
        cast(Union[str, List[str]], tag_values)
        tag_set.append({"Key": key, "Values": tag_values})

    # Check for existing bucket.
    return resource_generator(
        client=lookup_client,
        function_name="get_resources",
        resource_name="ResourceTagMappingList",
        TagFilters=tag_set,
        ResourceTypeFilters=resource_types,
    )


def tag_dict_to_aws(tags: Dict[str, str]) -> List[Dict[str, str]]:
    return [{"Key": cast(str, key), "Value": cast(str, value)} for key, value in tags.items()]
