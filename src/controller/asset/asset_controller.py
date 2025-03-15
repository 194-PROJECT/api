from flask import request
from core.api import Api, GetModelRequest, response

from database.model.asset import Asset, AssetKeyEnum, AssetKeyTypes
from src.handler.asset.asset_handler import AssetHandler

app = Api.application

@app.route('/asset/<int:id>', methods=['GET'])
def get_asset(id: int):
    asset = AssetHandler.get_asset(id)

    if not asset:
        return response(
            message="Asset not found",
            code=404,
            errors=["Failed to retrieve the requested asset"],
        )

    return response(
        message=f"Asset {asset.name} found",
        code=200,
        data=asset.model_dump()
    )

@app.route('/asset', methods=['GET'])
def get_assets():
    get_request = GetModelRequest.model_validate(dict(request.args), context={
        'model': Asset,
        'table_keys': AssetKeyEnum,
        'key_types': AssetKeyTypes,
    })

    assets = AssetHandler.get_assets(
        get_request.limit,
        get_request.offset,
        get_request.order_by_clause,
        get_request.where_clause,
    )

    if not assets or not len(assets):
        return response(
            message="No assets found",
            code=404,
            errors=["Failed to retrieve any assets"],
        )

    return response(
        message="Assets found",
        code=200,
        data=[asset.model_dump() for asset in assets]
    )

@app.route('/asset', methods=['POST'])
def create_asset():
    asset_data = request.json
    new_asset = AssetHandler.create_asset(asset_data)
    
    if not new_asset:
        return response(
            message="Failed to create asset",
            code=400,
            errors=["Failed to create asset from the provided data"],
        )

    return response(
        message=f"Asset {new_asset.name} created",
        code=201,
        data=new_asset.model_dump()
    )

@app.route('/asset/<int:id>', methods=['PUT'])
def update_asset(id: int):
    asset = AssetHandler.get_asset(id)

    if not asset:
        return response(
            message="Asset not found",
            code=404,
            errors=["Cannot update asset that does not exist"]
        )

    asset_update_request = asset.model_copy(update=request.json)
    updated_asset = AssetHandler.update_asset(id, asset_update_request)
    
    return response(
        message=f"Asset {updated_asset.name} updated",
        code=200,
        data=updated_asset.model_dump()
    )

@app.route('/asset/<int:id>', methods=['DELETE'])
def delete_asset(id: int):
    asset = AssetHandler.get_asset(id)
    
    if not asset:
        return response(
            message="Asset not found",
            code=404,
            errors=["Cannot delete asset that does not exist"],
        )
    
    AssetHandler.delete_asset(id)
    
    return response(
        message=f"Asset {asset.name} deleted",
        code=200
    )

@app.route('/asset', methods=['DELETE'])
def delete_assets():
    asset_ids = request.args.getlist('ids', type=int)

    if not isinstance(asset_ids, list) or not all(isinstance(id, int) for id in asset_ids):
        return response(
            message="Invalid course ids provided",
            code=400,
            errors=["Asset ids must be a list of integers"],
        )

    if not asset_ids or not len(asset_ids):
        return response(
            message="No asset ids provided",
            code=400,
            errors=["No asset ids provided"],
        )

    AssetHandler.delete_assets_by_id(asset_ids)
    
    return response(
        message="Assets deleted",
        code=200
    )
