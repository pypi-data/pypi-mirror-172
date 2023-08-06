"""State module for AWS Neptune DB Parameter group."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    db_parameter_group_family: str,
    parameters: List = None,
    resource_id: str = None,
    description: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
) -> Dict[str, Any]:
    """Creates a new DB parameter group.

    A DB parameter group is initially created with the default parameters for the
    database engine used by the DB instance. To provide custom values for any of the parameters, you must modify the
    group after creating it using ModifyDBParameterGroup. Once you've created a DB parameter group, you need to
    associate it with your DB instance using ModifyDBInstance. When you associate a new DB parameter group with a
    running DB instance, you need to reboot the DB instance without failover for the new DB parameter group and
    associated settings to take effect.  After you create a DB parameter group, you should wait at least 5 minutes
    before creating your first DB instance that uses that DB parameter group as the default parameter group. This
    allows Amazon Neptune to fully complete the create action before the parameter group is used as the default for
    a new DB instance. This is especially important for parameters that are critical when creating the default
    database for a DB instance, such as the character set for the default database defined by the
    character_set_database parameter. You can use the Parameter Groups option of the Amazon Neptune console or the
    DescribeDBParameters command to verify that your DB parameter group has been created or modified.

    Args:
        name(str):
            An idem name of the resource.
        db_parameter_group_family(str):
            The DB parameter group family name. A DB parameter group can be associated with one and only one
            DB parameter group family, and can be applied only to a DB instance running a database engine
            and engine version compatible with that DB parameter group family.
        parameters(list, Optional):
            An array of parameter names, values, and the apply method for the parameter update.
            At least one parameter name, value, and apply method must be supplied; subsequent arguments are optional. Defaults to None.
        resource_id(str, Optional):
            AWS DBParameterGroup Name. Defaults to None.
        description(str):
            The description for the DB parameter group.
        tags(dict or list, Optional):
            Dict in the format of {tag-key: tag-value} or List of tags in the format of
            [{"Key": tag-key, "Value": tag-value}] to associate with the DB parameter group.
            Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * Value(str, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_neptune_db_parameter_group]:
                aws.neptune.db_parameter_group.present:
                    - name: 'string'
                    - db_parameter_group_family: 'string'
                    - parameters:
                        - AllowedValues: 'string'
                          ApplyMethod: 'string'
                          ApplyType: 'string'
                          DataType: 'string'
                          Description: 'string'
                          IsModifiable: 'string'
                          MinimumEngineVersion: 'string'
                          ParameterName: 'string'
                          ParameterValue: 'string'
                          Source: 'string'
                    - resource_id: 'string'
                    - description: 'string'
                    - tags:
                        - Key: 'string'
                          Value: 'string'
                        - Key: 'string'
                          Value: 'string'

    Returns:
        Dict[str, Dict[str,Any]]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.neptune.db_parameter_group.present:
                - name: value
                - db_parameter_group_name: value
                - db_parameter_group_family: value
                - description: value
                - parameters:
                  - AllowedValues: 10-2147483647
                    ApplyMethod: pending-reboot
                    ApplyType: static
                    DataType: integer
                    Description: Graph query timeout (ms).
                    IsModifiable: true
                    MinimumEngineVersion: 1.0.1.0
                    ParameterName: neptune_query_timeout
                    ParameterValue: '120001'
                    Source: user
    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if resource_id:
        before = await hub.exec.boto3.client.neptune.describe_db_parameter_groups(
            ctx, DBParameterGroupName=resource_id
        )
        if not before["result"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

    if before and before["ret"].get("DBParameterGroups"):
        resource_arn = before["ret"]["DBParameterGroups"][0].get("DBParameterGroupArn")
        old_tags = await hub.tool.aws.neptune.tag.get_tags_for_resource(
            ctx, resource_arn=resource_arn
        )
        if not old_tags["result"]:
            result["result"] = False
            result["comment"] = old_tags["comment"]
            return result
        old_tags = old_tags["ret"]
        parameter_ret = await hub.exec.boto3.client.neptune.describe_db_parameters(
            ctx, DBParameterGroupName=resource_id
        )
        if not parameter_ret["result"]:
            result["result"] = False
            result["comment"] = parameter_ret["comment"]
            return result
        resource_translated = hub.tool.aws.neptune.db_parameter_group.convert_raw_db_parameter_group_to_present(
            before["ret"]["DBParameterGroups"][0],
            idem_resource_name=resource_id,
            tags=old_tags,
            parameters=parameter_ret["ret"].get("Parameters"),
        )
        result["old_state"] = resource_translated
        plan_state = copy.deepcopy(result["old_state"])

        old_parameters = result["old_state"].get("parameters", [])
        if parameters and not hub.tool.aws.state_comparison_utils.are_lists_identical(
            old_parameters, parameters
        ):
            resource_updated = True
            if ctx.get("test", False):
                plan_state["parameters"] = parameters
            else:
                ret = await hub.exec.boto3.client.neptune.modify_db_parameter_group(
                    ctx, DBParameterGroupName=name, Parameters=parameters
                )
                result["result"] = ret["result"]
                result["comment"] = result["comment"] + ret["comment"]
                if not result["result"]:
                    return result
        if tags is not None and tags != old_tags:
            resource_updated = True
            update_ret = await hub.tool.aws.neptune.tag.update_tags(
                ctx=ctx,
                resource_arn=resource_arn,
                old_tags=old_tags,
                new_tags=tags,
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                hub.log.debug(
                    f"Failed updating tags for aws.neptune.db_parameter_group '{name}'"
                )
                return result
            result["comment"] = result["comment"] + update_ret["comment"]
            if ctx.get("test", False) and update_ret["ret"] is not None:
                plan_state["tags"] = update_ret["ret"]

        if ctx.get("test", False):
            if resource_updated:
                result["new_state"] = plan_state
                result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.neptune.db_parameter_group", name=name
                )
            else:
                result["comment"] = (
                    f"aws.neptune.db_parameter_group '{name}' already exists",
                )
                result["new_state"] = copy.deepcopy(result["old_state"])
            return result
        if not resource_updated:
            result["comment"] = (
                f"aws.neptune.db_parameter_group '{name}' already exists",
            )
        else:
            result["comment"] = result["comment"] + (
                f"Updated aws.neptune.db_parameter_group '{name}'",
            )
    else:
        if ctx.get("test", False):
            # when a db_parameter_group is created aws will set some default parameters
            # this may change in the future so this code returns a fake parameter group
            default_parameters = [
                {
                    "AllowedValues": "fake",
                    "ApplyMethod": "pending-reboot",
                    "ApplyType": "static",
                    "DataType": "string",
                    "Description": "fake",
                    "IsModifiable": True,
                    "MinimumEngineVersion": "1.1.1.0",
                    "ParameterName": "fake_parameter",
                    "ParameterValue": "fake",
                    "Source": "fake",
                }
            ]
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": resource_id,
                    "tags": tags,
                    "description": description,
                    "db_parameter_group_family": db_parameter_group_family,
                    "parameters": parameters if parameters else default_parameters,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.neptune.db_parameter_group", name=name
            )
            return result
        ret = await hub.exec.boto3.client.neptune.create_db_parameter_group(
            ctx,
            DBParameterGroupName=name,
            DBParameterGroupFamily=db_parameter_group_family,
            Description=description,
            Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
            if tags
            else None,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        resource_id = ret["ret"]["DBParameterGroup"]["DBParameterGroupName"]
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.neptune.db_parameter_group", name=name
        )
        if parameters:
            # have to modify it after creation to add the parameters
            # cant create it with the parameters
            ret = await hub.exec.boto3.client.neptune.modify_db_parameter_group(
                ctx, DBParameterGroupName=name, Parameters=parameters
            )
            result["result"] = ret["result"]
            result["comment"] = result["comment"] + ret["comment"]
            if not result["result"]:
                return result
    if (not before) or resource_updated:
        after = await hub.exec.boto3.client.neptune.describe_db_parameter_groups(
            ctx, DBParameterGroupName=resource_id
        )
        if not (after["result"] and after["ret"].get("DBParameterGroups")):
            result["result"] = False
            result["comment"] = result["comment"] + after["comment"]
            return result
        resource_arn = (
            after["ret"].get("DBParameterGroups")[0].get("DBParameterGroupArn")
        )
        tags = await hub.tool.aws.neptune.tag.get_tags_for_resource(
            ctx, resource_arn=resource_arn
        )
        if not tags["result"]:
            result["result"] = False
            result["comment"] = result["comment"] + tags["comment"]
            return result
        tags = tags["ret"]
        parameter_ret = await hub.exec.boto3.client.neptune.describe_db_parameters(
            ctx, DBParameterGroupName=resource_id
        )
        if not parameter_ret["result"]:
            result["result"] = False
            result["comment"] = result["comment"] + parameter_ret["comment"]
            return result
        resource_translated = hub.tool.aws.neptune.db_parameter_group.convert_raw_db_parameter_group_to_present(
            after["ret"].get("DBParameterGroups")[0],
            idem_resource_name=name,
            parameters=parameter_ret["ret"].get("Parameters"),
            tags=tags,
        )
        result["new_state"] = resource_translated
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes a specified DBParameterGroup.

    The DBParameterGroup to be deleted can't be associated with any DB
    instances.

    Args:
        name(str):
            An idem name of the resource.
        resource_id(str, Optional):
            AWS Neptune DB Parameter Group Name. Defaults to None
            Idem automatically considers this resource as absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_neptune_db_parameter_group]:
                aws.neptune.db_parameter_group.absent:
                    - name: 'string'
                    - resource_id: 'string'

    Returns:
        Dict[str, Dict[str,Any]]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.neptune.db_parameter_group.absent:
                - name: value
                - resource_id: value
    """
    already_absent_msg = hub.tool.aws.comment_utils.already_absent_comment(
        resource_type="aws.neptune.db_parameter_group", name=name
    )
    result = dict(
        comment=already_absent_msg,
        old_state=None,
        new_state=None,
        name=name,
        result=True,
    )

    if not resource_id:
        return result

    before = await hub.exec.boto3.client.neptune.describe_db_parameter_groups(
        ctx, DBParameterGroupName=resource_id
    )
    db_parameter_groups = (
        before["ret"].get("DBParameterGroups") if before.get("ret") else None
    )

    if not (before["result"] and db_parameter_groups):
        # This condition means an error other than the resource not being found has happened
        if not ("DBParameterGroupNotFoundFault" in str(before["comment"])):
            result["comment"] = before["comment"]
            result["result"] = False
        return result

    resource_arn = db_parameter_groups[0].get("DBParameterGroupArn")
    tags = await hub.tool.aws.neptune.tag.get_tags_for_resource(
        ctx, resource_arn=resource_arn
    )
    if not tags["result"]:
        result["result"] = False
        result["comment"] = tags["comment"]
        return result
    tags = tags["ret"]
    parameter_ret = await hub.exec.boto3.client.neptune.describe_db_parameters(
        ctx, DBParameterGroupName=resource_id
    )
    if not parameter_ret["result"]:
        result["result"] = False
        result["comment"] = parameter_ret["comment"]
        return result
    resource_translated = hub.tool.aws.neptune.db_parameter_group.convert_raw_db_parameter_group_to_present(
        db_parameter_groups[0],
        idem_resource_name=resource_id,
        tags=tags,
        parameters=parameter_ret["ret"].get("Parameters"),
    )
    result["old_state"] = resource_translated

    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.neptune.db_parameter_group", name=name
        )
    else:
        ret = await hub.exec.boto3.client.neptune.delete_db_parameter_group(
            ctx, DBParameterGroupName=resource_id
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.neptune.db_parameter_group", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns a list of DBParameterGroup descriptions.

    Returns:
        Dict[str, Dict[str,Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.neptune.db_parameter_group
    """
    result = {}
    ret = await hub.exec.boto3.client.neptune.describe_db_parameter_groups(ctx)

    if not ret["result"]:
        hub.log.debug(f"Could not describe db_parameter_group {ret['comment']}")
        return {}

    for db_parameter_group in ret["ret"]["DBParameterGroups"]:
        resource_id = db_parameter_group.get("DBParameterGroupName")
        resource_arn = db_parameter_group.get("DBParameterGroupArn")
        tags = await hub.tool.aws.neptune.tag.get_tags_for_resource(
            ctx, resource_arn=resource_arn
        )
        if not tags["result"]:
            # if something goes wrong fetching the tags (not if the tags are None that is a normal path)
            hub.log.warning(
                f"Failed listing tags for aws.neptune.db_parameter_group '{resource_id}'"
                f"Describe will skip this aws.neptune.db_parameter_group and continue. "
            )
            continue
        parameter_ret = await hub.exec.boto3.client.neptune.describe_db_parameters(
            ctx, DBParameterGroupName=resource_id
        )
        if not parameter_ret["result"]:
            hub.log.warning(
                f"Failed listing parameters for aws.neptune.db_parameter_group '{resource_id}'"
                f"Describe will skip this aws.neptune.db_parameter_group and continue. "
            )
            continue
        tags = tags["ret"]
        resource_translated = hub.tool.aws.neptune.db_parameter_group.convert_raw_db_parameter_group_to_present(
            db_parameter_group,
            idem_resource_name=resource_id,
            parameters=parameter_ret["ret"].get("Parameters"),
            tags=tags,
        )
        result[resource_id] = {
            "aws.neptune.db_parameter_group.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
