from flask import request
from core.api import Api, GetModelRequest, response

from database.model.groups import Group, GroupKeyEnum, GroupKeyTypes
from src.dto.group.group_dto import GroupDTO
from src.handler.group.group_handler import GroupHandler

app = Api.application

@app.route('/group/<int:id>', methods=['GET'])
def get_group(id: int):
    group = GroupHandler.get_group(id)

    if not group:
        return response(
            message="Group not found",
            code=404,
            errors=["Failed to retrieve the requested group"],
        )

    return response(
        message=f"Group {group.name} found",
        code=200,
        data=group.model_dump()
    )

@app.route('/group', methods=['GET'])
def get_groups():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Group,
        'table_keys': GroupKeyEnum,
        'key_types': GroupKeyTypes,
    })

    groups = GroupHandler.get_groups(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if not groups or not len(groups):
        return response(
            message="No groups found",
            code=404,
            errors=["Failed to retrieve any groups"],
        )

    group_count = GroupHandler.get_group_count(get_request.where_clause)

    return response(
        message="Groups found",
        code=200,
        data=[group.model_dump() for group in groups],
        page=get_request.page,
        total_rows=group_count,
    )

@app.route('/group/count', methods=['GET'])
def get_group_count():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Group,
        'table_keys': GroupKeyEnum,
        'key_types': GroupKeyTypes,
    })

    group_count = GroupHandler.get_group_count(get_request.where_clause)

    return response(
        message="Group count found",
        code=200,
        data=group_count
    )

@app.route('/group', methods=['POST'])
def create_group():
    group_data = GroupDTO(**request.json)
    group = GroupHandler.create_group(group_data)
    
    if not group:
        return response(
            message="Failed to create group",
            code=400,
            errors=["Failed to create the group with the provided data"],
        )

    return response(
        message=f"Group {group.name} created",
        code=201,
        data=group.model_dump()
    )

@app.route('/group/<int:id>', methods=['PATCH'])
def update_group(id: int):
    group = GroupHandler.get_group(id)

    if not group:
        return response(
            message="Group not found",
            code=404,
            errors=["Failed to retrieve the requested group for update"],
        )

    group_update_request = group.model_copy(update=request.json)
    updated_group = GroupHandler.update_group(id, group_update_request)
    
    return response(
        message=f"Group {updated_group.name} updated",
        code=200,
        data=updated_group.model_dump()
    )

@app.route('/group/<int:id>', methods=['DELETE'])
def delete_group(id: int):
    group = GroupHandler.get_group(id)
    
    if not group:
        return response(
            message="Group not found",
            code=404,
            errors=["Failed to retrieve the requested group for deletion"],
        )
    
    GroupHandler.delete_group(id)
    
    return response(
        message=f"Group {group.name} deleted",
        code=200
    )

@app.route('/group', methods=['DELETE'])
def delete_groups():
    group_ids = request.args.getlist('ids', type=int)

    if not isinstance(group_ids, list) or not all(isinstance(id, int) for id in group_ids):
        return response(
            message="Invalid group ids provided",
            code=400,
            errors=["Group ids must be a list of integers"],
        )

    if not group_ids or not len(group_ids):
        return response(
            message="No group ids provided",
            code=400,
            errors=["Please provide a list of group ids to delete"],
        )

    GroupHandler.delete_groups_by_id(group_ids)
    
    return response(
        message="Groups deleted",
        code=200
    )
