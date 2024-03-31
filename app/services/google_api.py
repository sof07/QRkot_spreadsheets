from datetime import datetime
from fastapi import HTTPException, status

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"
MAXIMUM_NUMBER_OF_ROWS = 100
MAXIMUM_NUMBER_OF_COLUMNS = 11


def table_range(row_range, column_range):
    if row_range < MAXIMUM_NUMBER_OF_ROWS and column_range < MAXIMUM_NUMBER_OF_COLUMNS:
        return f"R1C1:R{row_range}C{column_range}"
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Размер данных превышает максимально допустимый размер таблицы",
    )


def create_table_values():
    now_date_time = datetime.now().strftime(FORMAT)
    return [
        ["Отчёт от", now_date_time],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]


def create_spreadsheet_properties():
    now_date_time = datetime.now().strftime(FORMAT)
    return {
        "properties": {"title": f"Отчёт от {now_date_time}", "locale": "ru_RU"},
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Лист1",
                    "gridProperties": {"rowCount": 100, "columnCount": 11},
                }
            }
        ],
    }


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover("sheets", "v4")
    spreadsheet_body = create_spreadsheet_properties()
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response["spreadsheetId"]
    return spreadsheet_id


async def set_user_permissions(spreadsheetid: str, wrapper_services: Aiogoogle) -> None:
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str, charity_project: list, wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover("sheets", "v4")
    table_values = create_table_values()
    for project in charity_project:
        time = project.close_date - project.create_date
        new_row = [
            str(project.name),
            str(time),
            str(project.description),
        ]
        table_values.append(new_row)
    row_range = len(table_values)
    column_range = len(max(table_values, key=len))
    update_body = {"majorDimension": "ROWS", "values": table_values}
    response = await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=table_range(row_range, column_range),
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
    return response
